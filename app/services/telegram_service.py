import requests
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_order_alert(order: dict):
    customer = order["customerInfo"]
    services = order["service_detail"]

    items_text = ""
    for s in services:
        items_text += (
            f"🍽 {s['service_name']}\n"
            f"Qty: {s['quantity']} | "
            f"Price: ${s['total_price']}\n\n"
        )

    message = f"""
🛎 *NEW ORDER RECEIVED*

👤 *Customer*: {customer['fullName']}
📞 *Phone*: {customer['phone']}
📍 *Address*: {customer['address']}

🧾 *Order Details*
{items_text}

💰 *Total*: ${order['totalAmount']}

⏰ Please start preparing the order.
"""

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(TELEGRAM_URL, json=payload)
    response.raise_for_status()
