import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(course):
    """Create product in stripe"""
    return stripe.Product.create(name=course)


def create_stripe_price(amount, product):
    """Create price in stripe"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product.get('id'),
    )


def create_stripe_session(price):
    """Create session for payment in stripe"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
