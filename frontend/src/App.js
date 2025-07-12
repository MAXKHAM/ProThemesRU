import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider } from 'next-themes';
import { AuthProvider } from './contexts/AuthContext';
import { TemplateProvider } from './contexts/TemplateContext';
import { EditorProvider } from './contexts/EditorContext';
import RoutesComponent from './routes';
import './styles/App.css';

function App() {
  return (
    <Router>
      <ThemeProvider attribute="class" defaultTheme="light">
        <AuthProvider>
          <TemplateProvider>
            <EditorProvider>
              <RoutesComponent />
            </EditorProvider>
          </TemplateProvider>
        </AuthProvider>
      </ThemeProvider>
    </Router>
  );
}

export default App;
