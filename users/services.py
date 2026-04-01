import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course):
    """Создаёт продукт в Stripe."""
    return stripe.Product.create(
        name=course.title,
        description=course.description,
    )

def create_stripe_price(product_id, amount, currency='rub'):
    """Создаёт цену (сумма в рублях, конвертируется в копейки)."""
    return stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency=currency,
    )

def create_checkout_session(price_id, success_url, cancel_url):
    """Создаёт сессию оплаты."""
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )

def retrieve_session(session_id):
    """Возвращает данные сессии по id."""
    return stripe.checkout.Session.retrieve(session_id)