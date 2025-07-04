from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Order

orders_bp = Blueprint('orders_bp', __name__, url_prefix='/orders')

@orders_bp.route('/my_orders')
@login_required
def my_orders():
    """Страница с заказами пользователя."""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders) 