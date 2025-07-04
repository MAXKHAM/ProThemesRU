class HtmlBlock:
    """Базовый класс для HTML блоков"""
    def __init__(self, block_id: str, **kwargs):
        self.block_id = block_id
        self.attributes = kwargs.get('attributes', {})
        self.css_classes = kwargs.get('css_classes', [])
        self.styles = kwargs.get('styles', {})
    
    def _get_attributes_string(self) -> str:
        """Генерирует строку атрибутов для HTML элемента"""
        attrs = []
        if self.css_classes:
            attrs.append(f'class="{" ".join(self.css_classes)}"')
        if self.styles:
            style_str = "; ".join([f"{k}: {v}" for k, v in self.styles.items()])
            attrs.append(f'style="{style_str}"')
        for key, value in self.attributes.items():
            attrs.append(f'{key}="{value}"')
        return " ".join(attrs)
    
    def render(self) -> str:
        """Метод для рендеринга блока - должен быть переопределен в дочерних классах"""
        raise NotImplementedError("Метод render должен быть переопределен")

class CalculatorBlock(HtmlBlock):
    """Блок для простого калькулятора сложения двух чисел."""
    def __init__(self, block_id: str, title: str = "Калькулятор", **kwargs):
        super().__init__(block_id, **kwargs)
        self.title = title

    def render(self) -> str:
        return f"""
        <section {self._get_attributes_string()}>
            <h2>{self.title}</h2>
            <form id='calc-form'>
                <input type='number' id='a' placeholder='Число 1'>
                <input type='number' id='b' placeholder='Число 2'>
                <button type='button' onclick="document.getElementById('calc-result').innerText = Number(document.getElementById('a').value) + Number(document.getElementById('b').value)">Сложить</button>
            </form>
            <div id='calc-result'></div>
        </section>
        """

class HeaderBlock(HtmlBlock):
    """Блок заголовка сайта"""
    def __init__(self, block_id: str, title: str = "Заголовок сайта", **kwargs):
        super().__init__(block_id, **kwargs)
        self.title = title

    def render(self) -> str:
        return f"""
        <header {self._get_attributes_string()}>
            <h1>{self.title}</h1>
        </header>
        """

class HeroSectionBlock(HtmlBlock):
    """Блок главной секции (hero)"""
    def __init__(self, block_id: str, title: str = "Добро пожаловать", subtitle: str = "Создавайте потрясающие сайты", **kwargs):
        super().__init__(block_id, **kwargs)
        self.title = title
        self.subtitle = subtitle

    def render(self) -> str:
        return f"""
        <section {self._get_attributes_string()}>
            <div class="hero-content">
                <h1>{self.title}</h1>
                <p>{self.subtitle}</p>
                <button class="cta-button">Начать</button>
            </div>
        </section>
        """

class TextBlock(HtmlBlock):
    """Блок с текстом"""
    def __init__(self, block_id: str, title: str = "Заголовок", content: str = "Текст блока", **kwargs):
        super().__init__(block_id, **kwargs)
        self.title = title
        self.content = content

    def render(self) -> str:
        return f"""
        <div {self._get_attributes_string()}>
            <h2>{self.title}</h2>
            <p>{self.content}</p>
        </div>
        """

class ImageBlock(HtmlBlock):
    """Блок с изображением"""
    def __init__(self, block_id: str, src: str = "https://via.placeholder.com/400x300", alt: str = "Изображение", **kwargs):
        super().__init__(block_id, **kwargs)
        self.src = src
        self.alt = alt

    def render(self) -> str:
        return f"""
        <div {self._get_attributes_string()}>
            <img src="{self.src}" alt="{self.alt}" style="max-width: 100%; height: auto;">
        </div>
        """

class ButtonBlock(HtmlBlock):
    """Блок с кнопкой"""
    def __init__(self, block_id: str, text: str = "Кнопка", url: str = "#", **kwargs):
        super().__init__(block_id, **kwargs)
        self.text = text
        self.url = url

    def render(self) -> str:
        return f"""
        <div {self._get_attributes_string()}>
            <a href="{self.url}" class="button">{self.text}</a>
        </div>
        """

class FooterBlock(HtmlBlock):
    """Блок подвала"""
    def __init__(self, block_id: str, text: str = "© 2024 ProThemesRU", **kwargs):
        super().__init__(block_id, **kwargs)
        self.text = text

    def render(self) -> str:
        return f"""
        <footer {self._get_attributes_string()}>
            <p>{self.text}</p>
        </footer>
        """

class WebsitePage:
    """Класс для представления страницы сайта"""
    def __init__(self, page_id: str, title: str = "Новая страница"):
        self.page_id = page_id
        self.title = title
        self.blocks = []
    
    def add_block(self, block: HtmlBlock):
        """Добавляет блок на страницу"""
        self.blocks.append(block)
    
    def render(self) -> str:
        """Рендерит всю страницу"""
        blocks_html = "\n".join([block.render() for block in self.blocks])
        return f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; }}
                .hero-content {{ text-align: center; padding: 80px 20px; background: linear-gradient(45deg, #667eea, #764ba2); color: white; }}
                .cta-button {{ padding: 15px 30px; background: white; color: #333; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; margin-top: 20px; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
                footer {{ background: #333; color: white; text-align: center; padding: 20px; }}
            </style>
        </head>
        <body>
            {blocks_html}
        </body>
        </html>
        """ 