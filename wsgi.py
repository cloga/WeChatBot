from main import load_config
from bot.wecom_bot import WeComBot
import logging

# Load configuration (from env vars on Azure)
config = load_config()

# Ensure we are in WeCom mode for server deployment
if config['wechat'].get('mode') != 'wecom':
    logging.warning("Forcing mode to 'wecom' for WSGI deployment")
    config['wechat']['mode'] = 'wecom'

# Initialize the bot
bot = WeComBot(config)

# Expose the Flask app for Gunicorn
app = bot.app

if __name__ == "__main__":
    app.run()
