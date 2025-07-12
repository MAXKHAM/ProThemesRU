import React, { useState, useEffect } from 'react';
import '../styles/MediaPanel.css';

function MediaPanel({ isAdmin, updateElementProps, selectedElement }) {
  const [mediaFiles, setMediaFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  // Mock media files for demonstration
  useEffect(() => {
    setMediaFiles([
      { id: 1, name: 'image1.jpg', url: 'https://via.placeholder.com/150', type: 'image' },
      { id: 2, name: 'image2.png', url: 'https://via.placeholder.com/200', type: 'image' },
      { id: 3, name: 'logo.svg', url: 'https://via.placeholder.com/100', type: 'image' },
    ]);
  }, []);

  const handleFileUpload = async (event) => {
    const files = event.target.files;
    if (!files.length) return;

    setIsUploading(true);
    
    // Simulate file upload
    setTimeout(() => {
      const newFiles = Array.from(files).map((file, index) => ({
        id: Date.now() + index,
        name: file.name,
        url: URL.createObjectURL(file),
        type: file.type.startsWith('image/') ? 'image' : 'other'
      }));
      
      setMediaFiles(prev => [...prev, ...newFiles]);
      setIsUploading(false);
    }, 1000);
  };

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    if (selectedElement && selectedElement.type === 'image') {
      updateElementProps(selectedElement.id, { src: file.url, alt: file.name });
    }
  };

  const handleFileDelete = (fileId) => {
    setMediaFiles(prev => prev.filter(file => file.id !== fileId));
    if (selectedFile && selectedFile.id === fileId) {
      setSelectedFile(null);
    }
  };

  if (!isAdmin) return null;

  return (
    <div className="media-panel">
      <h3>Медиа библиотека</h3>
      
      <div className="upload-section">
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileUpload}
          disabled={isUploading}
          id="media-upload"
        />
        <label htmlFor="media-upload" className="upload-button">
          {isUploading ? 'Загрузка...' : 'Загрузить файлы'}
        </label>
      </div>

      <div className="media-grid">
        {mediaFiles.map(file => (
          <div
            key={file.id}
            className={`media-item ${selectedFile?.id === file.id ? 'selected' : ''}`}
            onClick={() => handleFileSelect(file)}
          >
            <img src={file.url} alt={file.name} />
            <div className="media-item-info">
              <span className="media-name">{file.name}</span>
              <button
                className="delete-button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleFileDelete(file.id);
                }}
              >
                ×
              </button>
            </div>
          </div>
        ))}
      </div>

      {selectedFile && (
        <div className="selected-file-info">
          <h4>Выбранный файл:</h4>
          <p>{selectedFile.name}</p>
          {selectedElement && selectedElement.type === 'image' && (
            <button
              className="apply-button"
              onClick={() => updateElementProps(selectedElement.id, { src: selectedFile.url, alt: selectedFile.name })}
            >
              Применить к выбранному элементу
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default MediaPanel; 