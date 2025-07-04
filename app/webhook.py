
from flask import Blueprint, request
import hmac
import hashlib
import os

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook/yookassa', methods=['POST'])
def yookassa_webhook():
    payload = request.data
    signature = request.headers.get('Content-HMAC-SHA256')
    secret = os.getenv('YOOKASSA_SECRET_KEY', 'test')

    if not signature:
        return "Missing signature", 400

    hash_check = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hash_check, signature):
        return "Invalid signature", 403

    return "Payment processed", 200
