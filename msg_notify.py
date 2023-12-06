import os
import pywhatkit
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Your Twilio Account SID and Auth Token
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

account_sid2 = os.environ['TWILIO_ACCOUNT_SID2']
auth_token2 = os.environ['TWILIO_AUTH_TOKEN2']

# Create a Twilio client
# client = Client(account_sid, auth_token)

# Your WhatsApp number (sandbox number)
from_whatsapp_number = f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}'

# The recipient's WhatsApp number (your number)
to_whatsapp_number = f'whatsapp:{os.environ["MY_WHATSAPP_NUMBER"]}'

# Message content
message_body = "Your automation reached a certain stage."

# Send the WhatsApp message
message = Client.messages.create(
    from_=from_whatsapp_number,
    body=message_body,
    to=to_whatsapp_number
)

print("Message sent:", message.sid)

# pywhatkit.sendwhatmsg_instantly(
                # "+541157101241", "Se consiguió turno :D")