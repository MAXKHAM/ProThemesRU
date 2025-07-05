#!/usr/bin/env python3
"""
ProThemesRU Telegram Bot - Webhook Setup
Sets up webhook for Render deployment
"""

import os
import logging
from telegram import Bot
import requests

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL')

def set_webhook():
    """Set webhook for the bot"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not configured!")
        return False
    
    if not RENDER_EXTERNAL_URL:
        logger.error("RENDER_EXTERNAL_URL not configured!")
        return False
    
    bot = Bot(token=BOT_TOKEN)
    webhook_url = f"{RENDER_EXTERNAL_URL}/webhook"
    
    try:
        # Set webhook
        success = bot.set_webhook(url=webhook_url)
        if success:
            logger.info(f"Webhook set successfully to {webhook_url}")
            
            # Get webhook info
            webhook_info = bot.get_webhook_info()
            logger.info(f"Webhook info: {webhook_info}")
            
            return True
        else:
            logger.error("Failed to set webhook")
            return False
            
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return False

def delete_webhook():
    """Delete webhook for the bot"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not configured!")
        return False
    
    bot = Bot(token=BOT_TOKEN)
    
    try:
        success = bot.delete_webhook()
        if success:
            logger.info("Webhook deleted successfully")
            return True
        else:
            logger.error("Failed to delete webhook")
            return False
            
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")
        return False

def get_webhook_info():
    """Get webhook information"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not configured!")
        return None
    
    bot = Bot(token=BOT_TOKEN)
    
    try:
        webhook_info = bot.get_webhook_info()
        logger.info(f"Webhook info: {webhook_info}")
        return webhook_info
        
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        return None

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'set':
            set_webhook()
        elif command == 'delete':
            delete_webhook()
        elif command == 'info':
            get_webhook_info()
        else:
            print("Usage: python webhook_bot.py [set|delete|info]")
    else:
        # Default: set webhook
        set_webhook() 