from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.get("/templates", response_model=List[schemas.Template])
async def get_templates(
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Получить список шаблонов"""
    templates = db.query(models.Template).all()
    
    if category:
        templates = [t for t in templates if t.category == category]
    if featured is not None:
        templates = [t for t in templates if t.is_featured == featured]
    
    return templates

@router.get("/templates/{template_id}", response_model=schemas.Template)
async def get_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Получить конкретный шаблон"""
    template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.post("/templates", response_model=schemas.Template)
async def create_template(
    template: schemas.TemplateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Создать новый шаблон"""
    db_template = models.Template(
        **template.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        user_id=current_user.id
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.put("/templates/{template_id}", response_model=schemas.Template)
async def update_template(
    template_id: str,
    template: schemas.TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Обновить шаблон"""
    db_template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if db_template.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for key, value in template.dict().items():
        if value is not None:
            setattr(db_template, key, value)
    
    db_template.updated_at = datetime.now()
    db.commit()
    db.refresh(db_template)
    return db_template

@router.delete("/templates/{template_id}")
async def delete_template(
    template_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Удалить шаблон"""
    db_template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if db_template.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(db_template)
    db.commit()
    return {"message": "Template deleted successfully"}
