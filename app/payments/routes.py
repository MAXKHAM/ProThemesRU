import os
import uuid
from flask import Blueprint, request, redirect, url_for, session, flash, current_app, jsonify, render_template
from flask_login import login_required, current_user
from yookassa import Configuration, Payment as YooKassaPayment
from app.models import Payment, User
from app import db
from config import Config

payments_bp = Blueprint('payments', __name__)

# Настройка ЮKassa
Configuration.account_id = Config.YOOKASSA_SHOP_ID
Configuration.secret_key = Config.YOOKASSA_SECRET_KEY

@payments_bp.route('/create_payment', methods=['POST'])
@login_required
def create_payment():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите для оплаты.', 'warning')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    amount = float(request.form.get('amount', 100.0))  # Например, 100 рублей за PRO
    description = request.form.get('description', 'Оплата PRO-аккаунта')
    
    # Создаем запись о платеже в вашей БД со статусом "pending"
    new_payment = Payment(user_id=user_id, amount=amount, description=description, status='pending')
    db.session.add(new_payment)
    db.session.commit()
    
    # Создаем платеж в ЮKassa
    try:
        payment_request = YooKassaPayment.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": url_for('payments.payment_success', _external=True)  # Куда вернется пользователь
            },
            "capture": True,
            "description": description,
            "metadata": {
                "db_payment_id": new_payment.id  # Передаем ID из вашей БД для связывания
            },
            "receipt": {  # Пример чека
                "customer": {
                    "email": User.query.get(user_id).email
                },
                "items": [
                    {
                        "description": description,
                        "quantity": "1.00",
                        "amount": {
                            "value": str(amount),
                            "currency": "RUB"
                        },
                        "vat_code": "2",  # Без НДС
                        "payment_mode": "full_prepayment",
                        "payment_subject": "service"
                    }
                ]
            }
        }, uuid.uuid4())  # idempotence_key для избежания дублирования
        
        # Сохраняем ID платежа ЮKassa в вашей БД
        new_payment.payment_id = payment_request.id
        db.session.commit()
        
        return redirect(payment_request.confirmation.confirmation_url)
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при создании платежа: {e}', 'danger')
        return redirect(url_for('auth.dashboard'))

@payments_bp.route('/payment_webhook', methods=['POST'])
def payment_webhook():
    # Обработка вебхуков от ЮKassa
    # ЮKassa отправит сюда уведомление об изменении статуса платежа
    event_json = request.get_json()
    if event_json['event'] == 'payment.succeeded':
        payment_id = event_json['object']['id']
        db_payment_id = event_json['object']['metadata']['db_payment_id']
        
        payment_record = Payment.query.get(db_payment_id)
        if payment_record and payment_record.payment_id == payment_id:
            payment_record.status = 'succeeded'
            db.session.commit()
            # Здесь можно обновить статус пользователя до PRO
            user = User.query.get(payment_record.user_id)
            # user.is_pro = True  # Пример поля в модели User
            # db.session.commit()
    elif event_json['event'] == 'payment.canceled':
        # Обработка отмены платежа
        pass
    
    return 'OK', 200

@payments_bp.route('/payment_success')
def payment_success():
    flash('Платеж успешно обработан! Спасибо за покупку.', 'success')
    return redirect(url_for('main.index'))

@payments_bp.route('/create-pro-payment')
@login_required
def create_pro_payment():
    """Создание платежа для PRO подписки"""
    # Здесь будет логика создания платежа
    flash('Функция платежей пока в разработке', 'info')
    return redirect(url_for('main.index'))

@payments_bp.route('/cancel')
def payment_cancel():
    """Отмененный платеж"""
    return render_template('payment_cancel.html') 