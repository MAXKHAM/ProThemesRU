#!/usr/bin/env python3
"""
ProThemesRU Application Runner
This script provides an easy way to run the application in different modes.
"""

import os
import sys
import argparse
from app import app, db
from flask_migrate import upgrade

def create_admin_user():
    """Create a default admin user if none exists"""
    from app import User
    from werkzeug.security import generate_password_hash
    
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@prothemesru.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created: admin@prothemesru.com / admin123")

def init_database():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        upgrade()
        create_admin_user()
        print("✅ Database initialized successfully")

def run_development():
    """Run the application in development mode"""
    print("🚀 Starting ProThemesRU in development mode...")
    app.run(debug=True, host='0.0.0.0', port=5000)

def run_production():
    """Run the application in production mode"""
    print("🚀 Starting ProThemesRU in production mode...")
    app.run(host='0.0.0.0', port=5000)

def run_tests():
    """Run the test suite"""
    import pytest
    print("🧪 Running tests...")
    pytest.main(['tests/'])

def main():
    parser = argparse.ArgumentParser(description='ProThemesRU Application Runner')
    parser.add_argument('--mode', choices=['dev', 'prod', 'init', 'test'], 
                       default='dev', help='Run mode')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    
    args = parser.parse_args()
    
    if args.mode == 'init':
        init_database()
    elif args.mode == 'test':
        run_tests()
    elif args.mode == 'prod':
        app.run(host=args.host, port=args.port)
    else:  # dev mode
        app.run(debug=True, host=args.host, port=args.port)

if __name__ == '__main__':
    main() 