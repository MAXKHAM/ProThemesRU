#!/usr/bin/env python3
"""
Test script to verify deployment readiness
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import flask_sqlalchemy
        print("✓ Flask-SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"✗ Flask-SQLAlchemy import failed: {e}")
        return False
    
    try:
        import flask_jwt_extended
        print("✓ Flask-JWT-Extended imported successfully")
    except ImportError as e:
        print(f"✗ Flask-JWT-Extended import failed: {e}")
        return False
    
    try:
        import flask_cors
        print("✓ Flask-CORS imported successfully")
    except ImportError as e:
        print(f"✗ Flask-CORS import failed: {e}")
        return False
    
    try:
        import werkzeug
        print("✓ Werkzeug imported successfully")
    except ImportError as e:
        print(f"✗ Werkzeug import failed: {e}")
        return False
    
    try:
        import dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ python-dotenv import failed: {e}")
        return False
    
    try:
        import requests
        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ requests import failed: {e}")
        return False
    
    return True

def test_app_startup():
    """Test if the Flask app can start without errors"""
    print("\nTesting app startup...")
    
    try:
        # Add the api directory to the path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))
        
        # Import the app
        from app import app
        
        # Test app creation
        with app.app_context():
            print("✓ Flask app created successfully")
            print("✓ App context works")
            
            # Test database connection
            from app import db
            db.engine.execute("SELECT 1")
            print("✓ Database connection works")
            
        return True
        
    except Exception as e:
        print(f"✗ App startup failed: {e}")
        return False

def main():
    """Run all tests"""
    print("ProThemesRU Deployment Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        sys.exit(1)
    
    # Test app startup
    if not test_app_startup():
        print("\n❌ App startup test failed!")
        sys.exit(1)
    
    print("\n✅ All tests passed! Deployment should work.")
    print("\nReady to deploy to Vercel!")

if __name__ == "__main__":
    main() 