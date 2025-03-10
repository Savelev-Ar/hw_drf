import os

from config.settings import STRIPE_API_KEY
import requests


def create_product(name):
    """
    Функция создает продукт на сервисе Stripe.
    """
    headers = {'Authorization': STRIPE_API_KEY,
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'name': name}

    response = requests.post('https://api.stripe.com/v1/products', headers=headers, data=data)

    if response.status_code == 200:
        response_json = response.json()
        return response_json['id']


def create_price(price, prod_id):
    """
    Функция создает цену на продукт на сервисе Stripe.
    """
    headers = {
        'Authorization': os.getenv('STRIPE_API_KEY'),
        'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'currency': 'usd',
            'product': prod_id,
            'unit_amount': price * 90}

    response = requests.post('https://api.stripe.com/v1/prices', headers=headers, data=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json['id']


def create_session(price_id):
    """
    Функция создает сессию для оплаты на сервисе Stripe
    """
    headers = {
        'Authorization': os.getenv('STRIPE_API_KEY'),
        'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'line_items[0][price]': price_id,
            'line_items[0][quantity]': 1,
            'mode': 'payment',
            'success_url': 'https://example.com/success'}
    response = requests.post('https://api.stripe.com/v1/checkout/sessions', headers=headers, data=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json['url'], response_json['id']


def check_payment_status(payment_id):
    """
    Функция проверяет статус оплаты на сервисе Stripe
    """
    headers = {
        'Authorization': os.getenv('STRIPE_API_KEY'),
        'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.get('https://api.stripe.com/v1/checkout/sessions/'+payment_id,
                            headers=headers)

    if response.status_code == 200:
        return response.json()
