import React from 'react';
import Editor from './components/Editor';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1><i className="fas fa-palette"></i> Canvas Editor</h1>
        <p>Создавайте дизайны с помощью drag-and-drop редактора</p>
      </header>
      <main className="App-main">
        <Editor />
      </main>
    </div>
  );
}

export default App;
