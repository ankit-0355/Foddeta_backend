import smtplib
from email.message import EmailMessage
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def send_tiffin_provider_registration_email(registration: dict):
    """
    Send a registration confirmation email to a newly registered Tiffin Provider.
    
    registration dict should contain:
    - contact_name
    - email
    - phone_number
    - business_name
    - description
    - primary_location
    - business_image_url (optional)
    """
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f9f5ef; padding:20px;">
      <div style="max-width:600px; margin:auto; background:#ffffff; padding:25px; border-radius:8px; box-shadow: 0 0 15px rgba(0,0,0,0.1);">
        <h2 style="color:#d35400;">🍛 Tiffin Provider Registration Confirmed</h2>
        <p>Dear <strong>{registration['owner_name']}</strong>,</p>
        <p>Thank you for registering as a Tiffin Provider on Foodeta! Here are your submitted details:</p>

        <table width="100%" cellpadding="8" cellspacing="0" style="border-collapse:collapse; background:#f9f9f9; border-radius:4px;">
          <tr>
            <td><strong>Business / Service Name:</strong></td>
            <td>{registration['business_name']}</td>
          </tr>
          <tr>
            <td><strong>Description:</strong></td>
            <td>{registration['description']}</td>
          </tr>
          <tr>
            <td><strong>Primary Location:</strong></td>
            <td>{registration['address']}</td>
          </tr>
          <tr>
            <td><strong>Contact Phone:</strong></td>
            <td>{registration['phone_number']}</td>
          </tr>
          <tr>
            <td><strong>Email Address:</strong></td>
            <td>{registration['email']}</td>
          </tr>
          {"<tr><td><strong>Business Image URL:</strong></td><td>" + registration['image_url'] + "</td></tr>" if registration.get("image_url") else ""}
        </table>

        <p style="margin-top:20px;">
          Welcome to Foodeta! Your registration is complete, and you now have access to your personalized dashboard to manage your tiffin services.
          <a href='http://127.0.0.1:8080/login'>Access Your Dashboard</a>
        </p>

        <p style="margin-top:30px;">
          Warm regards,<br/>
          <strong>Foodeta Team</strong><br/>
          <span style="color:#999;">Authentic Indian tiffin service in Canada</span>
        </p>
      </div>
    </body>
    </html>
    """

    msg = EmailMessage()
    msg["Subject"] = "Foodeta Registration Confirmation"
    msg["From"] = SENDER_EMAIL
    msg["To"] = registration["email"]

    msg.set_content("Thank you for registering as a Tiffin Provider on Foodeta.")
    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
