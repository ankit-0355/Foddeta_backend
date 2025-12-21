import smtplib
from email.message import EmailMessage
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


def send_order_confirmation_email(order: dict):
    customer = order["customerInfo"]
    services = order["service_detail"]

    rows = ""
    for s in services:
        rows += f"""
        <tr>
            <td>{s['service_name']}</td>
            <td style="text-align:center;">{s['quantity']}</td>
            <td style="text-align:right;">${s['price_per_item']}</td>
            <td style="text-align:right;">${s['total_price']}</td>
        </tr>
        """

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">
      <div style="max-width:600px; margin:auto; background:#ffffff; padding:20px; border-radius:8px;">
        
        <h2 style="color:#ff6f00;">🍽️ Order Confirmed</h2>
        <p>Hi <strong>{customer['fullName']}</strong>,</p>
        <p>Thank you for your order! Here are your order details:</p>

        <table width="100%" cellpadding="8" cellspacing="0" style="border-collapse:collapse;">
          <thead>
            <tr style="background:#f8f8f8;">
              <th align="left">Service</th>
              <th align="center">Qty</th>
              <th align="right">Price</th>
              <th align="right">Total</th>
            </tr>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>

        <p style="margin-top:15px; font-size:16px;">
          <strong>Total Amount:</strong> ${order['totalAmount']}
        </p>

        <hr/>

        <p><strong>Delivery Address:</strong><br/>
        {customer['address']}</p>

        <p style="font-size:14px; color:#666;">
          We’ll contact you at <strong>{customer['phone']}</strong> if needed.
        </p>

        <p style="margin-top:20px;">
          Thanks for choosing <strong>Foodeta</strong> ❤️<br/>
          <span style="color:#999;">Fresh food, delivered.</span>
        </p>
      </div>
    </body>
    </html>
    """

    msg = EmailMessage()
    msg["Subject"] = "Your Foodeta Order Confirmation 🍱"
    msg["From"] = SENDER_EMAIL
    msg["To"] = customer["email"]

    msg.set_content("Your order has been placed successfully.")
    msg.add_alternative(html_content, subtype="html")

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
