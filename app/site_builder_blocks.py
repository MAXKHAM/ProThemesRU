import abc
from typing import Dict, List, Optional, Any

class HtmlBlock(abc.ABC):
    """
    Абстрактный базовый класс для всех HTML-блоков.
    Каждый блок должен уметь генерировать свой HTML-код.
    """
    def __init__(self, block_id: str, css_classes: Optional[List[str]] = None, attributes: Optional[Dict[str, str]] = None):
        self.block_id = block_id
        self.css_classes = css_classes or []
        self.attributes = attributes or {}

    def _get_attributes_string(self) -> str:
        """Генерирует строку HTML-атрибутов."""
        attrs = []
        if self.block_id:
            attrs.append(f'id="{self.block_id}"')
        if self.css_classes:
            attrs.append(f'class="{" ".join(self.css_classes)}"')
        for key, value in self.attributes.items():
            attrs.append(f'{key}="{value}"')
        return " ".join(attrs)

    @abc.abstractmethod
    def render(self) -> str:
        """
        Абстрактный метод, который должен быть реализован каждым подклассом
        для генерации HTML-кода блока.
        """
        pass

class HeaderBlock(HtmlBlock):
    """Блок для шапки сайта."""
    def __init__(self, block_id: str, logo_text: str, nav_items: Dict[str, str], **kwargs):
        super().__init__(block_id, **kwargs)
        self.logo_text = logo_text
        self.nav_items = nav_items

    def render(self) -> str:
        nav_links = "".join([f'<a href="{url}">{text}</a>' for text, url in self.nav_items.items()])
        return f"""
        <header {self._get_attributes_string()}>
            <div class="logo">{self.logo_text}</div>
            <nav>{nav_links}</nav>
        </header>        """

class HeroSectionBlock(HtmlBlock):
    """Блок для первого экрана с большим заголовком и кнопкой."""
    def __init__(self, block_id: str, title: str, subtitle: str, button_text: str, button_url: str, **kwargs):
        super().__init__(block_id, **kwargs)
        self.title = title
        self.subtitle = subtitle
        self.button_text = button_text
        self.button_url = button_url

    def render(self) -> str:
        return f"""
        <section {self._get_attributes_string()} class="hero-section">
            <div class="hero-content">
                <h1>{self.title}</h1>
                <p>{self.subtitle}</p>
                <a href="{self.button_url}" class="button">{self.button_text}</a>
            </div>
        </section>
        """

class TextBlock(HtmlBlock):
    """Блок для простого текстового содержимого."""
    def __init__(self, block_id: str, content: str, tag: str = "p", **kwargs):
        if tag not in ["p", "div", "span", "h1", "h2", "h3", "h4", "h5", "h6"]:
            raise ValueError(f"Unsupported HTML tag for TextBlock: {tag}")
        super().__init__(block_id, **kwargs)
        self.content = content
        self.tag = tag

    def render(self) -> str:
        return f"""
        <{self.tag} {self._get_attributes_string()} class="text-block {' '.join(self.css_classes)}">{self.content}</{self.tag}>
        """

class ImageBlock(HtmlBlock):
    """Блок для изображений."""
    def __init__(self, block_id: str, src: str, alt: str = "", width: Optional[int] = None, height: Optional[int] = None, **kwargs):
        super().__init__(block_id, **kwargs)
        self.src = src
        self.alt = alt
        self.width = width
        self.height = height

    def render(self) -> str:
        size_attrs = ""
        if self.width:
            size_attrs += f' width="{self.width}"'
        if self.height:
            size_attrs += f' height="{self.height}"'
        return f"""
        <img src="{self.src}" alt="{self.alt}" {size_attrs} {self._get_attributes_string()} class="{' '.join(self.css_classes)}">
        """

class ButtonBlock(HtmlBlock):
    """Блок для интерактивной кнопки."""
    def __init__(self, block_id: str, text: str, url: str, **kwargs):
        super().__init__(block_id, **kwargs)
        self.text = text
        self.url = url

    def render(self) -> str:
        return f"""
        <a href="{self.url}" {self._get_attributes_string()} class="button {' '.join(self.css_classes)}">{self.text}</a>
        """

class FooterBlock(HtmlBlock):
    """Блок для подвала сайта."""
    def __init__(self, block_id: str, copyright_text: str, **kwargs):
        super().__init__(block_id, **kwargs)
        self.copyright_text = copyright_text

    def render(self) -> str:
        return f"""
        <footer {self._get_attributes_string()} class="footer">
            <p>{self.copyright_text}</p>
        </footer>
        """

class WebsitePage:
    """
    Класс, представляющий одну веб-страницу, собранную из HTML-блоков.
    Это наш основной "конструктор" страниц.
    """
    def __init__(self, title: str, language: str = "ru"):
        self.title = title
        self.language = language
        self.blocks: List[HtmlBlock] = []
        self._default_styles = """
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; color: #333; }
            header { background-color: #333; color: white; padding: 1em 2em; display: flex; justify-content: space-between; align-items: center; }
            header .logo { font-size: 1.5em; font-weight: bold; }
            header nav a { color: white; margin-left: 20px; text-decoration: none; }
            section { padding: 4em 2em; text-align: center; }
            .hero-section { background-color: #007bff; color: white; }
            .hero-content h1 { font-size: 3em; margin-bottom: 0.5em; }
            .hero-content p { font-size: 1.2em; max-width: 600px; margin: 0 auto 2em; }
            .button { display: inline-block; background-color: #28a745; color: white; padding: 0.8em 1.5em; text-decoration: none; border-radius: 5px; transition: background-color 0.3s ease; }
            .button:hover { background-color: #218838; }
            .text-block { max-width: 800px; margin: 2em auto; line-height: 1.6; }
            img { max-width: 100%; height: auto; border-radius: 8px; }
            footer { background-color: #333; color: white; text-align: center; padding: 1em 0; margin-top: 4em; }
        </style>
        """

    def add_block(self, block: HtmlBlock):
        """Добавляет HTML-блок на страницу."""
        if not isinstance(block, HtmlBlock):
            raise TypeError("Only instances of HtmlBlock can be added to a page.")
        self.blocks.append(block)

    def render(self) -> str:
        """Генерирует полный HTML-код страницы."""
        body_content = "\n".join([block.render() for block in self.blocks])
        return f"""<!DOCTYPE html>
<html lang="{self.language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    {self._default_styles}
</head>
<body>
{body_content}
</body>
</html>
""" 