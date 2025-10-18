# app.py -- Twilio WhatsApp sender (requires Twilio setup)
from flask import Flask, request, render_template_string, redirect, url_for
from twilio.rest import Client
import os

app = Flask(__name__)

# Set these as environment variables for safety, or paste temporarily:
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID") or "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN") or "your_auth_token"
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM") or "whatsapp:+14155238886"  # Twilio sandbox or approved number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

INDEX_HTML = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>NK EDITOR - WhatsApp (Twilio)</title>
<style>
body{background:#000;color:#00ff66;font-family:monospace;padding:20px}
.container{max-width:600px;margin:0 auto;background:rgba(0,10,0,0.85);padding:18px;border-radius:10px;border:1px solid #003300}
input,textarea{width:100%;padding:8px;margin:8px 0;background:transparent;color:#00ff66;border:1px solid #004400;border-radius:6px}
.btn{background:#00ff66;color:#000;padding:10px;border:none;border-radius:6px;font-weight:bold}
.small{color:#99ffb3;font-size:12px}
</style>
</head>
<body>
<div class="container">
<h2>🔥 NK EDITOR - Twilio WhatsApp Sender</h2>
<p class="small">Requires valid Twilio credentials and a WhatsApp-enabled Twilio number</p>
<form method="post" enctype="multipart/form-data">
<label>Target number (E.164, e.g. +919876543210)</label>
<input name="to_number" required>
<label>Message</label>
<textarea name="message" rows="4" required></textarea>
<button class="btn" type="submit">Send via Twilio</button>
</form>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        to_number = request.form.get("to_number").strip()
        message = request.form.get("message").strip()
        if not to_number or not message:
            return "Missing fields", 400

        try:
            sent = client.messages.create(
                from_=TWILIO_WHATSAPP_FROM,
                body=message,
                to=f"whatsapp:{to_number}"
            )
            return f"Message sent. SID: {sent.sid} <br><a href='/'>Back</a>"
        except Exception as e:
            return f"Error sending message: {e} <br><a href='/'>Back</a>"
    return render_template_string(INDEX_HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5040)
