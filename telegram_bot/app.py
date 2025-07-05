#!/usr/bin/env python3
"""
ProThemesRU Telegram Bot - Main Application
Deployment-ready Flask application for Render
"""

import os
import logging
from flask import Flask, request, jsonify
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')

def load_templates():
    """Load templates from JSON files"""
    try:
        with open('templates/blocks/premium_templates.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Templates file not found, using default")
        return {
            "premium_templates": [
                {
                    "id": 1,
                    "name": "Современный SaaS Лендинг",
                    "category": "saas",
                    "price": 15000,
                    "description": "Премиум лендинг для SaaS продуктов"
                },
                {
                    "id": 2,
                    "name": "Креативное Агентство",
                    "category": "agency",
                    "price": 12000,
                    "description": "Стильный сайт для креативных агентств"
                },
                {
                    "id": 3,
                    "name": "Премиум E-commerce",
                    "category": "ecommerce",
                    "price": 25000,
                    "description": "Полнофункциональный интернет-магазин"
                }
            ]
        }

# Flask routes
@app.route('/')
def home():
    """Home page"""
    return jsonify({
        "status": "success",
        "message": "ProThemesRU Telegram Bot is running!",
        "version": "1.0.0",
        "templates_count": len(load_templates().get('premium_templates', [])),
        "endpoints": {
            "webhook": "/webhook",
            "health": "/health",
            "status": "/status",
            "templates": "/templates"
        }
    })

@app.route('/templates')
def templates():
    """Get templates list"""
    templates_data = load_templates()
    return jsonify(templates_data)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle webhook from Telegram"""
    try:
        data = request.get_json()
        logger.info(f"Received webhook: {data}")
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "bot_token": "configured" if BOT_TOKEN else "missing",
        "admin_chat_id": "configured" if ADMIN_CHAT_ID else "missing"
    })

@app.route('/status')
def status():
    """Status endpoint"""
    return jsonify({
        "status": "running",
        "bot_token": "configured" if BOT_TOKEN else "missing",
        "templates_loaded": len(load_templates().get('premium_templates', []))
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 