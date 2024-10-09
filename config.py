import os

# OpenAI API Key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your_openai_api_key')
# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'your_telegram_bot_token')

# Twilio Auth Token and Account SID (if needed)
# TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'your_twilio_account_sid')
# TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'your_twilio_auth_token')

# Bot Prefix
BOT_PREFIX = 'yumyoda'

# Number of options to provide
NUM_OPTIONS = 10
