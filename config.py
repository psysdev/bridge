import os 
from dotenv import load_dotenv

load_dotenv()

def fetch_id(var):
    val = os.getenv(var)
    if not val:
        raise RuntimeError(f"Environment Variable {var} not found!")
    try:
        return int(val)
    except ValueError:
        raise RuntimeError(f"{var} must contain valid integer!")    

token = os.getenv("bot_token")


if not token:
    raise RuntimeError("Bot token not found!")

gc_id = fetch_id("general_channel_id")
wc_id = fetch_id("welcome_channel_id")
rc_id = fetch_id("rules_channel_id")
hnfc_id = fetch_id("hnf_channel_id")