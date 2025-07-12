import React, { useState, useEffect, useCallback } from 'react';
import '../styles/ScrapePanel.css';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

function ScrapePanel({ isAdmin }) {
    const [scrapingProfiles, setScrapingProfiles] = useState([]);
    const [selectedProfileId, setSelectedProfileId] = useState('');
    const [targetUrl, setTargetUrl] = useState('');
    const [profileName, setProfileName] = useState('');
    const [sections, setSections] = useState([{ 
        id: Date.now(), 
        rootSelector: '', 
        outputFileName: 'index.html', 
        fields: [{ id: Date.now() + 1, name: '', selector: '', attribute: 'text' }], 
        outputTemplate: '<div><h2>{{{title}}}</h2><p>{{{description}}}</p></div>' 
    }]);
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [scrapedSiteLink, setScrapedSiteLink] = useState('');

    // NEW: Advanced Scraping Options
    const [followLinks, setFollowLinks] = useState(false);
    const [maxDepth, setMaxDepth] = useState(1);
    const [downloadAssets, setDownloadAssets] = useState(false);
    const [downloadImages, setDownloadImages] = useState(true);
    const [downloadCss, setDownloadCss] = useState(true);
    const [downloadJs, setDownloadJs] = useState(false); // JS can be tricky, default to false

    const fetchScrapingProfiles = useCallback(async () => {
        if (!isAdmin) return;
        const token = localStorage.getItem('access_token');
        if (!token) return;

        try {
            const response = await fetch(`${API_BASE_URL}/admin/scraping_profiles`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                setScrapingProfiles(data);
                if (data.length > 0) {
                    setSelectedProfileId(data[0].id);
                    loadProfile(data[0].id);
                } else {
                    setSelectedProfileId('');
                    resetForm();
                }
            } else {
                console.error('Failed to fetch scraping profiles:', await response.json());
                setMessage('Ошибка загрузки профилей.');
            }
        } catch (error) {
            console.error('Error fetching scraping profiles:', error);
            setMessage('Ошибка сети при загрузке профилей.');
        }
    }, [isAdmin]);

    useEffect(() => {
        fetchScrapingProfiles();
    }, [fetchScrapingProfiles]);

    const loadProfile = useCallback((profileId) => {
        const profile = scrapingProfiles.find(p => p.id === profileId);
        if (profile) {
            setProfileName(profile.name);
            setTargetUrl(profile.targetUrl);
            setSections(profile.sections);
            // NEW: Load advanced options
            setFollowLinks(profile.followLinks || false);
            setMaxDepth(profile.maxDepth || 1);
            setDownloadAssets(profile.downloadAssets || false);
            setDownloadImages(profile.downloadImages || true);
            setDownloadCss(profile.downloadCss || true);
            setDownloadJs(profile.downloadJs || false);
        }
    }, [scrapingProfiles]);

    useEffect(() => {
        if (selectedProfileId) {
            loadProfile(selectedProfileId);
        }
    }, [selectedProfileId, loadProfile]);

    const resetForm = () => {
        setProfileName('');
        setTargetUrl('');
        setSections([{ 
            id: Date.now(), 
            rootSelector: '', 
            outputFileName: 'index.html', 
            fields: [{ id: Date.now() + 1, name: '', selector: '', attribute: 'text' }], 
            outputTemplate: '<div><h2>{{{title}}}</h2><p>{{{description}}}</p></div>' 
        }]);
        // Reset advanced options
        setFollowLinks(false);
        setMaxDepth(1);
        setDownloadAssets(false);
        setDownloadImages(true);
        setDownloadCss(true);
        setDownloadJs(false);
        setMessage('');
        setScrapedSiteLink('');
    };

    const handleAddSection = () => {
        setSections(prev => [...prev, { 
            id: Date.now(), 
            rootSelector: '', 
            outputFileName: `page_${prev.length + 1}.html`, 
            fields: [{ id: Date.now() + 1, name: '', selector: '', attribute: 'text' }], 
            outputTemplate: '<div><h2>{{{title}}}</h2><p>{{{description}}}</p></div>' 
        }]);
    };

    const handleRemoveSection = (id) => {
        setSections(prev => prev.filter(s => s.id !== id));
    };

    const handleSectionChange = (id, field, value) => {
        setSections(prev => prev.map(s => s.id === id ? { ...s, [field]: value } : s));
    };

    const handleAddField = (sectionId) => {
        setSections(prev => prev.map(s => s.id === sectionId ? { 
            ...s, 
            fields: [...s.fields, { id: Date.now() + Math.random(), name: '', selector: '', attribute: 'text' }] 
        } : s));
    };

    const handleRemoveField = (sectionId, fieldId) => {
        setSections(prev => prev.map(s => s.id === sectionId ? { 
            ...s, 
            fields: s.fields.filter(f => f.id !== fieldId) 
        } : s));
    };

    const handleFieldChange = (sectionId, fieldId, field, value) => {
        setSections(prev => prev.map(s => s.id === sectionId ? { 
            ...s, 
            fields: s.fields.map(f => f.id === fieldId ? { ...f, [field]: value } : f) 
        } : s));
    };

    const handleSaveProfile = async () => {
        if (!profileName || !targetUrl || sections.length === 0) {
            setMessage('Заполните все обязательные поля: Имя профиля, Целевой URL и хотя бы одну секцию.');
            return;
        }
        if (sections.some(s => !s.rootSelector || s.fields.some(f => !f.name || !f.selector))) {
            setMessage('Все секции и поля должны быть заполнены.');
            return;
        }

        setIsLoading(true);
        setMessage('Сохранение профиля...');
        const token = localStorage.getItem('access_token');
        if (!token) {
            setMessage('Ошибка: Не авторизован.');
            setIsLoading(false);
            return;
        }

        const profileData = {
            id: selectedProfileId || Date.now().toString(),
            name: profileName,
            targetUrl: targetUrl,
            sections: sections,
            // NEW: Save advanced options
            followLinks,
            maxDepth,
            downloadAssets,
            downloadImages,
            downloadCss,
            downloadJs,
        };

        try {
            const response = await fetch(`${API_BASE_URL}/admin/scraping_profiles`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(profileData)
            });

            if (response.ok) {
                const result = await response.json();
                setMessage(`Профиль "${result.profile.name}" сохранен!`);
                setSelectedProfileId(result.profile.id);
                fetchScrapingProfiles();
            } else {
                const errorData = await response.json();
                setMessage(`Ошибка сохранения: ${errorData.msg || 'Неизвестная ошибка'}`);
            }
        } catch (error) {
            setMessage(`Ошибка сети: ${error.message}`);
            console.error('Network error during save:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDeleteProfile = async () => {
        if (!selectedProfileId || !window.confirm('Вы уверены, что хотите удалить этот профиль?')) {
            return;
        }
        setIsLoading(true);
        setMessage('Удаление профиля...');
        const token = localStorage.getItem('access_token');
        if (!token) {
            setMessage('Ошибка: Не авторизован.');
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/admin/scraping_profiles/${selectedProfileId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                setMessage('Профиль удален!');
                setSelectedProfileId('');
                resetForm();
                fetchScrapingProfiles();
            } else {
                const errorData = await response.json();
                setMessage(`Ошибка удаления: ${errorData.msg || 'Неизвестная ошибка'}`);
            }
        } catch (error) {
            setMessage(`Ошибка сети: ${error.message}`);
            console.error('Network error during delete:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleScrapeSite = async () => {
        if (!selectedProfileId) {
            setMessage('Пожалуйста, выберите профиль для скрапинга.');
            return;
        }
        if (!targetUrl) {
            setMessage('Целевой URL не может быть пустым.');
            return;
        }

        setIsLoading(true);
        setMessage('Начинаем скрапинг...');
        setScrapedSiteLink('');
        const token = localStorage.getItem('access_token');
        if (!token) {
            setMessage('Ошибка: Не авторизован.');
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/admin/scrape_site`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    url: targetUrl,
                    profileId: selectedProfileId,
                    // NEW: Send advanced options
                    followLinks,
                    maxDepth,
                    downloadAssets,
                    downloadImages,
                    downloadCss,
                    downloadJs,
                })
            });

            if (response.ok) {
                const result = await response.json();
                setMessage(`Скрапинг завершен! Страниц: ${result.scraped_pages_count}, Активов: ${result.downloaded_assets_count}.`);
                setScrapedSiteLink(result.base_url);
            } else {
                const errorData = await response.json();
                setMessage(`Ошибка скрапинга: ${errorData.msg || 'Неизвестная ошибка'}`);
            }
        } catch (error) {
            setMessage(`Ошибка сети: ${error.message}`);
            console.error('Network error during scrape:', error);
        } finally {
            setIsLoading(false);
        }
    };

    if (!isAdmin) {
        return (
            <div className="scrape-panel">
                <h3>Управление Скрапингом</h3>
                <p>Требуются права администратора для доступа к этой функции.</p>
            </div>
        );
    }

    return (
        <div className="scrape-panel">
            <h3>Управление Скрапингом</h3>

            <div className="profile-management">
                <h4>Управление Профилями</h4>
                <div className="form-group">
                    <label htmlFor="profileSelect">Выбрать профиль:</label>
                    <select
                        id="profileSelect"
                        value={selectedProfileId}
                        onChange={(e) => setSelectedProfileId(e.target.value)}
                    >
                        <option value="">-- Новый профиль --</option>
                        {scrapingProfiles.map(profile => (
                            <option key={profile.id} value={profile.id}>{profile.name}</option>
                        ))}
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="profileName">Имя профиля:</label>
                    <input
                        type="text"
                        id="profileName"
                        value={profileName}
                        onChange={(e) => setProfileName(e.target.value)}
                        placeholder="Например: Новости TechCrunch"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="targetUrl">Целевой URL:</label>
                    <input
                        type="text"
                        id="targetUrl"
                        value={targetUrl}
                        onChange={(e) => setTargetUrl(e.target.value)}
                        placeholder="https://example.com/blog"
                    />
                </div>
                <div className="button-group">
                    <button onClick={handleSaveProfile} disabled={isLoading}>
                        <i className="fas fa-save"></i> Сохранить Профиль
                    </button>
                    <button onClick={handleDeleteProfile} disabled={isLoading || !selectedProfileId}>
                        <i className="fas fa-trash"></i> Удалить Профиль
                    </button>
                    <button onClick={resetForm} disabled={isLoading}>
                        <i className="fas fa-plus"></i> Новый Профиль
                    </button>
                </div>
            </div>

            <hr />

            <div className="scraping-sections">
                <h4>Секции Скрапинга</h4>
                {sections.map((section, index) => (
                    <div key={section.id} className="section-item">
                        <h5>Секция {index + 1}</h5>
                        <div className="form-group">
                            <label>Корневой селектор (CSS):</label>
                            <input
                                type="text"
                                value={section.rootSelector}
                                onChange={(e) => handleSectionChange(section.id, 'rootSelector', e.target.value)}
                                placeholder=".article-item"
                            />
                        </div>
                        <div className="form-group">
                            <label>Имя файла вывода:</label>
                            <input
                                type="text"
                                value={section.outputFileName}
                                onChange={(e) => handleSectionChange(section.id, 'outputFileName', e.target.value)}
                                placeholder="output.html"
                            />
                        </div>
                        <div className="form-group">
                            <label>Шаблон вывода (HTML):</label>
                            <textarea
                                value={section.outputTemplate}
                                onChange={(e) => handleSectionChange(section.id, 'outputTemplate', e.target.value)}
                                rows="3"
                                placeholder="<div><h3>{{{title}}}</h3><img src='{{{image}}}' /></div>"
                            />
                        </div>

                        <h6>Поля для извлечения:</h6>
                        {section.fields.map((field, fieldIndex) => (
                            <div key={field.id} className="field-item">
                                <input
                                    type="text"
                                    value={field.name}
                                    onChange={(e) => handleFieldChange(section.id, field.id, 'name', e.target.value)}
                                    placeholder="Имя поля (например, title)"
                                />
                                <input
                                    type="text"
                                    value={field.selector}
                                    onChange={(e) => handleFieldChange(section.id, field.id, 'selector', e.target.value)}
                                    placeholder="Селектор (например, h2.title)"
                                />
                                <select
                                    value={field.attribute}
                                    onChange={(e) => handleFieldChange(section.id, field.id, 'attribute', e.target.value)}
                                >
                                    <option value="text">Текст</option>
                                    <option value="href">Ссылка (href)</option>
                                    <option value="src">Изображение (src)</option>
                                    <option value="alt">Alt текст</option>
                                    <option value="title">Title атрибут</option>
                                </select>
                                <button 
                                    onClick={() => handleRemoveField(section.id, field.id)}
                                    className="remove-field-btn"
                                >
                                    <i className="fas fa-times"></i>
                                </button>
                            </div>
                        ))}
                        <button onClick={() => handleAddField(section.id)} className="add-field-btn">
                            <i className="fas fa-plus"></i> Добавить поле
                        </button>
                        <button onClick={() => handleRemoveSection(section.id)} className="remove-section-btn">
                            <i className="fas fa-trash"></i> Удалить секцию
                        </button>
                    </div>
                ))}
                <button onClick={handleAddSection} className="add-section-btn">
                    <i className="fas fa-plus"></i> Добавить секцию
                </button>
            </div>

            <hr />

            <div className="advanced-options">
                <h4>Расширенные опции скрапинга</h4>
                <div className="options-grid">
                    <div className="option-item">
                        <label>
                            <input
                                type="checkbox"
                                checked={followLinks}
                                onChange={(e) => setFollowLinks(e.target.checked)}
                            />
                            Следовать по ссылкам
                        </label>
                    </div>
                    <div className="option-item">
                        <label>
                            Максимальная глубина:
                            <input
                                type="number"
                                min="1"
                                max="5"
                                value={maxDepth}
                                onChange={(e) => setMaxDepth(parseInt(e.target.value))}
                            />
                        </label>
                    </div>
                    <div className="option-item">
                        <label>
                            <input
                                type="checkbox"
                                checked={downloadAssets}
                                onChange={(e) => setDownloadAssets(e.target.checked)}
                            />
                            Загружать ресурсы
                        </label>
                    </div>
                    <div className="option-item">
                        <label>
                            <input
                                type="checkbox"
                                checked={downloadImages}
                                onChange={(e) => setDownloadImages(e.target.checked)}
                                disabled={!downloadAssets}
                            />
                            Загружать изображения
                        </label>
                    </div>
                    <div className="option-item">
                        <label>
                            <input
                                type="checkbox"
                                checked={downloadCss}
                                onChange={(e) => setDownloadCss(e.target.checked)}
                                disabled={!downloadAssets}
                            />
                            Загружать CSS файлы
                        </label>
                    </div>
                    <div className="option-item">
                        <label>
                            <input
                                type="checkbox"
                                checked={downloadJs}
                                onChange={(e) => setDownloadJs(e.target.checked)}
                                disabled={!downloadAssets}
                            />
                            Загружать JavaScript файлы
                        </label>
                    </div>
                </div>
            </div>

            <hr />

            <div className="scraping-actions">
                <h4>Действия</h4>
                <button onClick={handleScrapeSite} disabled={isLoading} className="scrape-btn">
                    <i className="fas fa-download"></i> Начать скрапинг
                </button>
                {scrapedSiteLink && (
                    <div className="scraped-link">
                        <p>Скрапинг завершен! <a href={scrapedSiteLink} target="_blank" rel="noopener noreferrer">Просмотреть результат</a></p>
                    </div>
                )}
            </div>

            {message && (
                <div className={`message ${message.includes('Ошибка') ? 'error' : 'success'}`}>
                    {message}
                </div>
            )}
        </div>
    );
}

export default ScrapePanel; 