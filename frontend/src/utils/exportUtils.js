const MAX_CONTAINER_WIDTH = 960; // Максимальная ширина для адаптивного контейнера

export function cssStringToObject(cssString) {
    const styles = {};
    if (!cssString) return styles;
    cssString = cssString.replace(/\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$/gm, '$1');
    const parts = cssString.split(';');
    parts.forEach(part => {
        const trimmedPart = part.trim();
        if (trimmedPart) {
            const colonIndex = trimmedPart.indexOf(':');
            if (colonIndex > 0) {
                const key = trimmedPart.substring(0, colonIndex).trim();
                const value = trimmedPart.substring(colonIndex + 1).trim();
                if (key && value) {
                    styles[key] = value;
                }
            }
        }
    });
    return styles;
}

export function objectToCssString(cssObject) {
    if (!cssObject) return "";
    return Object.entries(cssObject)
        .map(([key, value]) => `${key}: ${value}`)
        .join('; ') + (Object.keys(cssObject).length > 0 ? ';' : '');
}

export function generateHtmlCss(elements) {
    const elementMap = new Map(elements.map(el => [el.id, el]));
    const rootElements = elements.filter(el => !el.parentId);

    let minX = Infinity, minY = Infinity;
    let maxX = -Infinity, maxY = -Infinity;

    if (rootElements.length > 0) {
        rootElements.forEach(el => {
            minX = Math.min(minX, el.x);
            minY = Math.min(minY, el.y);
            maxX = Math.max(maxX, el.x + el.width);
            maxY = Math.max(maxY, el.y + el.height);
        });
    } else {
        minX = 0; minY = 0; maxX = MAX_CONTAINER_WIDTH; maxY = 300;
    }

    const originalDesignWidth = maxX - minX;
    const originalDesignHeight = maxY - minY;

    const scaleFactor = originalDesignWidth > MAX_CONTAINER_WIDTH && originalDesignWidth > 0
        ? MAX_CONTAINER_WIDTH / originalDesignWidth
        : 1;

    const scaledContainerHeight = originalDesignHeight * scaleFactor;

    let htmlContent = `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мой Сайт (ProThemesRU)</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* Базовые стили для элементов конструктора */
        .canvas-element {
            box-sizing: border-box;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Только для элементов, которые абсолютно позиционированы */
        .canvas-element[style*="position: absolute;"] {
             position: absolute; /* Добавляем явно, если стиль не переопределен Flexbox */
        }

        /* Для дочерних элементов внутри группы */
        .group-element > .canvas-element {
            /* Если родитель flex/grid, то position: absolute не нужен */
            /* Эти стили будут переопределены инлайн стилями, если displayMode не absolute */
        }

        .canvas-element > * {
            width: 100%;
            height: 100%;
            box-sizing: border-box;
        }

        .text-element {
            text-align: center;
            word-break: break-word;
            padding: 5px;
        }
        .image-element {
            display: block;
            object-fit: contain;
            max-width: 100%;
            height: auto;
        }
        .button-element {
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            white-space: nowrap;
        }
        .shape-element {
            /* background-color and border-radius are inline */
        }
    </style>
</head>
<body>
    <div id="main-content-area">
`;
    let cssContent = `
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 20px 0;
    box-sizing: border-box;
}

#main-content-area {
    position: relative;
    max-width: ${MAX_CONTAINER_WIDTH}px;
    width: 100%;
    margin: 0 auto;
    min-height: ${Math.max(scaledContainerHeight, 200)}px;
    background-color: #ffffff;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
}
`;
    // Рекурсивная функция для рендеринга элементов
    function renderElementHtmlAndCss(element) {
        const children = elements.filter(el => el.parentId === element.id);

        let inlineStyles = '';
        let elementClasses = 'canvas-element';

        // Определяем, является ли родительский элемент Flexbox-контейнером
        const parent = element.parentId ? elementMap.get(element.parentId) : null;
        const isChildOfFlexContainer = parent && parent.type === 'group' && parent.props.displayMode === 'flex';

        if (isChildOfFlexContainer) {
            // Если элемент является дочерним для Flexbox-контейнера,
            // мы не используем position: absolute, left, top.
            // Вместо этого, его ширина и высота станут flex-basis или min/max-width/height.
            // Для простоты, пока будем использовать width/height как есть.
            // Можно добавить flex-grow: 1; flex-shrink: 1; flex-basis: auto;
            // Или конкретно: flex-basis: ${element.width}px;
            inlineStyles += `width: ${element.width}px; height: ${element.height}px;`;
        } else {
            // Если не дочерний для Flexbox-контейнера (т.е. абсолютный или корневой)
            const elX = element.x;
            const elY = element.y;
            const newX = (element.parentId === null) ? (elX - minX) * scaleFactor : elX;
            const newY = (element.parentId === null) ? (elY - minY) * scaleFactor : elY;
            const newWidth = (element.parentId === null) ? element.width * scaleFactor : element.width;
            const newHeight = (element.parentId === null) ? element.height * scaleFactor : element.height;

            inlineStyles += `position: absolute; left: ${newX}px; top: ${newY}px; width: ${newWidth}px; height: ${newHeight}px;`;
        }

        // Добавляем пользовательские классы
        if (element.props.customClasses && element.props.customClasses.length > 0) {
            elementClasses += ` ${element.props.customClasses.join(' ')}`;
        }

        let innerHtml = '';
        switch (element.type) {
            case 'text':
                innerHtml = `<div class="text-element">${element.props.content || ''}</div>`;
                inlineStyles += ` font-size: ${element.props.fontSize || '16px'}; color: ${element.props.color || '#000000'};`;
                break;
            case 'image':
                innerHtml = `<img src="${element.props.src || ''}" alt="${element.props.alt || ''}" class="image-element">`;
                break;
            case 'button':
                innerHtml = `<button class="button-element">${element.props.label || ''}</button>`;
                inlineStyles += ` background-color: ${element.props.bgColor || '#007bff'}; color: ${element.props.textColor || '#ffffff'};`;
                break;
            case 'shape':
                innerHtml = `<div class="shape-element"></div>`;
                inlineStyles += ` background-color: ${element.props.bgColor || '#ffc107'}; border-radius: ${element.props.borderRadius || '0'};`;
                break;
            case 'group':
                elementClasses += ' group-element';
                if (element.props.displayMode === 'flex') {
                    inlineStyles += ` display: flex;`;
                    if (element.props.flexDirection) inlineStyles += ` flex-direction: ${element.props.flexDirection};`;
                    if (element.props.justifyContent) inlineStyles += ` justify-content: ${element.props.justifyContent};`;
                    if (element.props.alignItems) inlineStyles += ` align-items: ${element.props.alignItems};`;
                    if (element.props.gap) inlineStyles += ` gap: ${element.props.gap};`;
                    // Группа с flexbox не имеет background-color/border-radius по умолчанию
                    // Если нужно, их можно добавить через customStyles
                } else {
                    // Если группа в абсолютном режиме
                    inlineStyles += ` position: absolute;`; // Явно указываем absolute для группы
                    inlineStyles += ` background-color: rgba(255, 255, 255, 0.05); border: 1px dashed rgba(0, 0, 0, 0.1);`;
                }

                // Рекурсивно рендерим детей
                innerHtml = children.map(child => renderElementHtmlAndCss(child)).join('\n');
                break;
            default:
                innerHtml = `<div>Неизвестный элемент</div>`;
        }

        // Добавляем пользовательские инлайн-стили в конце, чтобы они переопределяли предыдущие
        if (element.props.customStyles) {
            inlineStyles += ` ${objectToCssString(element.props.customStyles)}`;
        }

        return `        <div id="${element.id}" class="${elementClasses}" style="${inlineStyles}">${innerHtml}</div>`;
    }

    htmlContent += rootElements.map(el => renderElementHtmlAndCss(el)).join('\n');

    htmlContent += `    </div>
</body>
</html>`;

    return { htmlContent, cssContent };
} 