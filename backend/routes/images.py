from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from PIL import Image, ImageOps
from io import BytesIO
import os
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user
from ..config import settings

router = APIRouter()

@router.post("/images/optimize", response_model=schemas.OptimizedImage)
async def optimize_image(
    image_url: str,
    width: int = 800,
    height: int = 600,
    quality: int = 85,
    format: str = "webp",
    db: Session = Depends(get_db)
):
    """Оптимизация изображения"""
    try:
        # Загрузка изображения
        response = requests.get(image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Не удалось загрузить изображение")

        # Конвертация в PIL
        image = Image.open(BytesIO(response.content))

        # Оптимизация
        optimized_image = ImageOps.exif_transpose(image)
        optimized_image = optimized_image.convert("RGB")
        optimized_image = optimized_image.resize((width, height), Image.Resampling.LANCZOS)

        # Сохранение в оптимизированном формате
        output = BytesIO()
        optimized_image.save(
            output,
            format=format.upper(),
            quality=quality,
            optimize=True,
            progressive=True
        )

        # Сохранение в кэше
        cache_key = f"optimized_{hash(image_url)}_{width}_{height}_{quality}_{format}"
        cache_path = os.path.join(settings.IMAGE_CACHE_DIR, f"{cache_key}.{format}")
        
        with open(cache_path, 'wb') as f:
            f.write(output.getvalue())

        # Генерация URL
        optimized_url = f"/images/cache/{cache_key}.{format}"

        return {
            "original_url": image_url,
            "optimized_url": optimized_url,
            "width": width,
            "height": height,
            "format": format,
            "quality": quality
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/cache/{filename}")
async def get_cached_image(
    filename: str,
    db: Session = Depends(get_db)
):
    """Получение оптимизированного изображения из кэша"""
    cache_path = os.path.join(settings.IMAGE_CACHE_DIR, filename)
    
    if not os.path.exists(cache_path):
        raise HTTPException(status_code=404, detail="Изображение не найдено в кэше")

    return FileResponse(cache_path)
