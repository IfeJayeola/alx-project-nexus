import requests
from django.conf import settings

def initialize_chapa_payment(email, amount, first_name, last_name, tx_ref, callback_url):
    url = f"{settings.CHAPA_BASE_URL}/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "amount": str(amount),
        "first_name": first_name,
        "last_name": last_name,
        "tx_ref": tx_ref,
        "currency": "ETB",
        "callback_url": callback_url,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def verify_chapa_payment(tx_ref):
    url = f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}"
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()
