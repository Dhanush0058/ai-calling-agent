import os
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from twilio.rest import Client  # type: ignore

# Load environment variables from .env
load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_PHONE_NUMBER")

# Validate credentials
if not account_sid or "ACxxxx" in account_sid:
    print("Error: Please replace the TWILIO_ACCOUNT_SID placeholder in your .env file with your actual Account SID.")
    exit(1)
if not auth_token or "your_auth" in auth_token:
    print("Error: Please replace the TWILIO_AUTH_TOKEN placeholder in your .env file with your actual Auth Token.")
    exit(1)

to_number = "+919347249697"
url = "https://fanatic-arbitrate-aspect.ngrok-free.dev/voice/incoming"

print(f"Triggering outbound call from Twilio number ({from_number}) to your number ({to_number})...")
try:
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        url=url
    )
    print(f"Success! Call triggered. Call SID: {call.sid}")
except Exception as e:
    print(f"Failed to initiate call: {e}")
