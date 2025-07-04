import stripe
from flask import Blueprint, render_template, request, current_app, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Order
from app import db

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/payment')

@payment_bp.before_request
def set_api_key():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

@payment_bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    """Создает сессию оплаты в Stripe."""
    data = request.json
    if not data or not data.get('template_name') or not data.get('amount') or not data.get('html_content'):
        return jsonify({'error': 'Missing data'}), 400

    template_name = data['template_name']
    amount = float(data['amount'])
    html_content = data['html_content']

    new_order = Order(
        user_id=current_user.id,
        template_name=template_name,
        site_html=html_content,
        status='pending',
        price=amount
    )
    db.session.add(new_order)
    db.session.commit()

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': template_name,
                        'description': f'Сайт-шаблон: {template_name}',
                    },
                    'unit_amount': int(amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('payment_bp.payment_success', order_id=new_order.id, _external=True),
            cancel_url=url_for('payment_bp.payment_cancel', order_id=new_order.id, _external=True),
            metadata={
                'order_id': new_order.id,
                'user_id': current_user.id
            }
        )
        return jsonify({'sessionId': checkout_session.id})
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при создании сессии оплаты: {str(e)}', 'danger')
        return jsonify(error=str(e)), 403

@payment_bp.route('/payment-success')
def payment_success():
    """Страница успешной оплаты."""
    order_id = request.args.get('order_id')
    order = None
    if order_id:
        order = Order.query.get(order_id)
    flash('Оплата успешно завершена! Ваш сайт готов к загрузке.', 'success')
    return render_template('payment_success.html', order=order)

@payment_bp.route('/payment-cancel')
def payment_cancel():
    """Страница отмены оплаты."""
    order_id = request.args.get('order_id')
    order = None
    if order_id:
        order = Order.query.get(order_id)
    flash('Оплата отменена.', 'info')
    return render_template('payment_cancel.html')

@payment_bp.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Webhook для обработки событий Stripe."""
    payload = request.get_data()
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': str(e)}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata'].get('order_id')
        if order_id:
            with current_app.app_context():
                order = Order.query.get(order_id)
                if order:
                    order.status = 'completed'
                    db.session.commit()
                    print(f"Order {order_id} status updated to completed.")
                else:
                    print(f"Order {order_id} not found for webhook.")
        else:
            print("Order ID not found in session metadata.")

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        order_id = session['metadata'].get('order_id')
        if order_id:
            with current_app.app_context():
                order = Order.query.get(order_id)
                if order:
                    order.status = 'failed'
                    db.session.commit()
                    print(f"Order {order_id} status updated to failed.")

    return jsonify({'status': 'success'}), 200 