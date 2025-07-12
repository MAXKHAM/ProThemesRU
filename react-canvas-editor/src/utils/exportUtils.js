// exportUtils.js

export function cssStringToObject(cssString) {
    const styles = {};
    if (!cssString) {
        return styles;
    }
    // Remove comments
    cssString = cssString.replace(/\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$/gm, '$1');

    const parts = cssString.split(';');
    for (const part of parts) {
        const trimmedPart = part.trim();
        if (trimmedPart) {
            const [key, value] = trimmedPart.split(':', 2);
            if (key && value) {
                styles[key.trim()] = value.trim();
            }
        }
    }
    return styles;
}

export function objectToCssString(cssObject) {
    if (!cssObject) {
        return "";
    }
    return Object.entries(cssObject)
        .map(([key, value]) => `${key}: ${value}`)
        .join('; ');
}

// Updated to accept canvasSettings
export function generateHtmlCss(elements, canvasSettings = {}) {
    const MAX_CONTAINER_WIDTH = 960;

    const elementMap = new Map(elements.map(el => [el.id, el]));

    // Ensure all elements have a zIndex for sorting
    elements.forEach(el => {
        if (!el.props) el.props = {};
        if (el.props.zIndex === undefined) el.props.zIndex = 1;
    });

    const sortedElements = [...elements].sort((a, b) => (a.props.zIndex || 1) - (b.props.zIndex || 1));

    let minX = Infinity;
    let minY = Infinity;
    let maxX = -Infinity;
    let maxY = -Infinity;

    if (elements.length > 0) {
        elements.forEach(el => {
            // Need absolute positions for bounding box if elements are nested
            let abs_x = el.x;
            let abs_y = el.y;
            let current_parent = elementMap.get(el.parentId);
            while (current_parent) {
                abs_x += current_parent.x;
                abs_y += current_parent.y;
                current_parent = elementMap.get(current_parent.parentId);
            }

            minX = Math.min(minX, abs_x);
            minY = Math.min(minY, abs_y);
            maxX = Math.max(maxX, abs_x + el.width);
            maxY = Math.max(maxY, abs_y + el.height);
        });
    } else {
        minX = 0; minY = 0; maxX = MAX_CONTAINER_WIDTH; maxY = 300;
    }

    const original_design_width = maxX - minX;
    const original_design_height = maxY - minY;

    const scale_factor = original_design_width > MAX_CONTAINER_WIDTH && original_design_width > 0
        ? MAX_CONTAINER_WIDTH / original_design_width
        : 1;

    const scaled_container_height = original_design_height * scale_factor;

    let html_content = `<!DOCTYPE html>
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
        /* Only for elements that are absolutely positioned */
        .canvas-element[style*="position: absolute;"] {
             position: absolute;
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
    let css_content = `
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    /* Default background for body, can be overridden by main-content-area */
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
    min-height: ${Math.max(scaled_container_height, 200)}px;
    background-color: #ffffff; /* Default background, will be overridden by canvas settings if provided */
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
`;

    // Apply canvas background settings if provided
    if (canvasSettings.backgroundColor) {
        css_content += `    background-color: ${canvasSettings.backgroundColor};\n`;
    }
    if (canvasSettings.backgroundImage) {
        css_content += `    background-image: url('${canvasSettings.backgroundImage}');\n`;
        css_content += `    background-repeat: ${canvasSettings.backgroundRepeat || 'no-repeat'};\n`;
        css_content += `    background-size: ${canvasSettings.backgroundSize || 'cover'};\n`;
        css_content += `    background-position: ${canvasSettings.backgroundPosition || 'center center'};\n`;
    }

    css_content += `}

/* Responsive design */
@media (max-width: 768px) {
    #main-content-area {
        margin: 0 10px;
        border-radius: 4px;
    }
}

/* Element styles */
`;

    // Generate CSS for each element
    sortedElements.forEach((element, index) => {
        const elementId = `element-${element.id}`;
        
        // Calculate absolute position
        let abs_x = element.x;
        let abs_y = element.y;
        let current_parent = elementMap.get(element.parentId);
        while (current_parent) {
            abs_x += current_parent.x;
            abs_y += current_parent.y;
            current_parent = elementMap.get(current_parent.parentId);
        }

        // Scale positions
        const scaled_x = (abs_x - minX) * scale_factor;
        const scaled_y = (abs_y - minY) * scale_factor;
        const scaled_width = element.width * scale_factor;
        const scaled_height = element.height * scale_factor;

        // Add element to HTML
        html_content += `        <div id="${elementId}" class="canvas-element" style="position: absolute; left: ${scaled_x}px; top: ${scaled_y}px; width: ${scaled_width}px; height: ${scaled_height}px; z-index: ${element.props.zIndex || 1};`;

        // Add element-specific styles
        if (element.type === 'text') {
            html_content += ` font-size: ${element.props.fontSize || '16px'}; color: ${element.props.color || '#000000'};`;
            html_content += `">\n            <div class="text-element">${element.props.content || 'Текст'}</div>\n        </div>\n`;
        } else if (element.type === 'image') {
            html_content += `">\n            <img src="${element.props.src || 'https://via.placeholder.com/150'}" alt="${element.props.alt || 'Изображение'}" class="image-element">\n        </div>\n`;
        } else if (element.type === 'button') {
            html_content += ` background-color: ${element.props.bgColor || '#007bff'}; color: ${element.props.textColor || '#ffffff'};`;
            html_content += `">\n            <button class="button-element">${element.props.label || 'Кнопка'}</button>\n        </div>\n`;
        } else if (element.type === 'shape') {
            html_content += ` background-color: ${element.props.bgColor || '#ffc107'}; border-radius: ${element.props.borderRadius || '0'};`;
            html_content += `">\n            <div class="shape-element"></div>\n        </div>\n`;
        } else if (element.type === 'group') {
            html_content += ` display: ${element.props.displayMode || 'absolute'};`;
            if (element.props.displayMode === 'flex') {
                html_content += ` flex-direction: ${element.props.flexDirection || 'row'}; justify-content: ${element.props.justifyContent || 'flex-start'}; align-items: ${element.props.alignItems || 'stretch'}; gap: ${element.props.gap || '0px'};`;
            } else if (element.props.displayMode === 'grid') {
                html_content += ` grid-template-columns: ${element.props.gridTemplateColumns || '1fr'}; grid-template-rows: ${element.props.gridTemplateRows || 'auto'}; gap: ${element.props.gridGap || '0px'};`;
            }
            html_content += ` background-color: ${element.props.backgroundColor || 'rgba(255, 255, 255, 0.05)'}; border: ${element.props.borderWidth || '1px'} ${element.props.borderStyle || 'dashed'} ${element.props.borderColor || 'rgba(0, 0, 0, 0.1)'};`;
            html_content += `">\n            <div class="group-content">Группа элементов</div>\n        </div>\n`;
        }

        // Generate CSS for element
        css_content += `#${elementId} {\n`;
        
        // Add custom styles
        if (element.props.customStyles) {
            Object.entries(element.props.customStyles).forEach(([key, value]) => {
                css_content += `    ${key}: ${value};\n`;
            });
        }

        // Add border styles
        if (element.props.borderWidth && element.props.borderWidth !== '0px') {
            css_content += `    border: ${element.props.borderWidth} ${element.props.borderStyle || 'solid'} ${element.props.borderColor || '#000000'};\n`;
        }

        // Add box shadow
        if (element.props.boxShadowX && element.props.boxShadowX !== '0px') {
            const shadow = `${element.props.boxShadowX} ${element.props.boxShadowY || '0px'} ${element.props.boxShadowBlur || '0px'} ${element.props.boxShadowSpread || '0px'} ${element.props.boxShadowColor || 'rgba(0,0,0,0.2)'}`;
            css_content += `    box-shadow: ${shadow};\n`;
        }

        // Add background styles
        if (element.props.backgroundColor) {
            css_content += `    background-color: ${element.props.backgroundColor};\n`;
        }
        if (element.props.backgroundImage) {
            css_content += `    background-image: url('${element.props.backgroundImage}');\n`;
            css_content += `    background-repeat: ${element.props.backgroundRepeat || 'no-repeat'};\n`;
            css_content += `    background-size: ${element.props.backgroundSize || 'cover'};\n`;
            css_content += `    background-position: ${element.props.backgroundPosition || 'center center'};\n`;
        }

        // Add custom classes
        if (element.props.customClasses && element.props.customClasses.length > 0) {
            css_content += `    /* Custom classes: ${element.props.customClasses.join(' ')} */\n`;
        }

        css_content += `}\n\n`;
    });

    html_content += `    </div>
</body>
</html>`;

    return { html: html_content, css: css_content };
} 