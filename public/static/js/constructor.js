// Конструктор сайтов
const Constructor = {
    init() {
        this.setupEventListeners();
        this.loadBlocks();
        this.setupPreview();
    },

    setupEventListeners() {
        // Добавление блока
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-block-btn')) {
                this.addBlock(e.target.dataset.blockType);
            }
        });

        // Выбор блока
        document.addEventListener('click', (e) => {
            if (e.target.closest('.block')) {
                this.selectBlock(e.target.closest('.block'));
            }
        });

        // Двойной клик для редактирования текста
        document.addEventListener('dblclick', (e) => {
            if (e.target.closest('.editable')) {
                this.editText(e.target.closest('.editable'));
            }
        });
    },

    loadBlocks() {
        // Загрузка доступных блоков из API
        fetch('/api/blocks')
            .then(response => response.json())
            .then(blocks => {
                this.renderBlocks(blocks);
            });
    },

    renderBlocks(blocks) {
        const blocksContainer = document.querySelector('.blocks-container');
        blocks.forEach(block => {
            const blockElement = document.createElement('div');
            blockElement.className = 'block-preview';
            blockElement.innerHTML = `
                <div class="block-preview-content">
                    ${block.html}
                </div>
                <button class="add-block-btn" data-block-type="${block.type}">
                    Добавить
                </button>
            `;
            blocksContainer.appendChild(blockElement);
        });
    },

    addBlock(type) {
        // Добавление блока в редактор
        const block = this.getBlockTemplate(type);
        const editor = document.querySelector('.editor-content');
        const newBlock = document.createElement('div');
        newBlock.className = 'block';
        newBlock.innerHTML = block.html;
        editor.appendChild(newBlock);
    },

    getBlockTemplate(type) {
        // Получение шаблона блока
        const blocks = {
            'header': {
                html: `
                    <header class="block-header">
                        <nav>
                            <div class="logo">Logo</div>
                            <ul class="nav-links">
                                <li><a href="#">Главная</a></li>
                                <li><a href="#">О нас</a></li>
                                <li><a href="#">Услуги</a></li>
                                <li><a href="#">Контакты</a></li>
                            </ul>
                        </nav>
                    </header>
                `,
                styles: {
                    backgroundColor: '#ffffff',
                    padding: '20px',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }
            },
            'hero': {
                html: `
                    <section class="block-hero">
                        <div class="hero-content">
                            <h1 class="editable">Заголовок</h1>
                            <p class="editable">Описание</p>
                            <button class="cta-button">Подробнее</button>
                        </div>
                    </section>
                `,
                styles: {
                    backgroundColor: '#f8fafc',
                    minHeight: '400px',
                    padding: '40px'
                }
            },
            // Добавьте другие типы блоков...
        };
        return blocks[type];
    },

    selectBlock(block) {
        // Выбор блока для редактирования
        document.querySelectorAll('.block').forEach(b => b.classList.remove('selected'));
        block.classList.add('selected');
        this.updatePropertiesPanel(block);
    },

    updatePropertiesPanel(block) {
        // Обновление панели свойств
        const properties = document.querySelector('.properties-panel');
        properties.innerHTML = `
            <h3>Свойства блока</h3>
            <div class="property-group">
                <label>Фон</label>
                <input type="color" value="#ffffff">
            </div>
            <div class="property-group">
                <label>Паддинг</label>
                <input type="number" value="20">
            </div>
        `;
    },

    editText(element) {
        // Редактирование текста
        const originalText = element.textContent;
        const input = document.createElement('input');
        input.type = 'text';
        input.value = originalText;
        input.className = 'edit-input';
        
        element.replaceWith(input);
        
        input.addEventListener('blur', () => {
            element.textContent = input.value;
            input.replaceWith(element);
        });
    },

    setupPreview() {
        // Настройка превью
        const preview = document.querySelector('.preview');
        preview.innerHTML = `
            <div class="preview-content">
                <div id="editor-content" class="editor-content">
                    <!-- Содержимое редактора -->
                </div>
            </div>
        `;
    }
};

// Инициализация конструктора
document.addEventListener('DOMContentLoaded', () => {
    Constructor.init();
});
