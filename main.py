import yaml
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_config(path='config/config.yaml'):
    # 1. Try loading from file
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    # 2. Fallback to Environment Variables (Best for Azure/Docker)
    logging.info("Config file not found, using Environment Variables.")
    return {
        'wechat': {
            'mode': os.environ.get('WECHAT_MODE', 'wecom'),
            'bot_name': os.environ.get('BOT_NAME', 'Cloga'),
            'trigger_word': os.environ.get('TRIGGER_WORD', '@Jarvis'),
            'wecom': {
                'token': os.environ.get('WECOM_TOKEN'),
                'encoding_aes_key': os.environ.get('WECOM_ENCODING_AES_KEY'),
                'corp_id': os.environ.get('WECOM_CORP_ID'),
                'secret': os.environ.get('WECOM_SECRET'),
                'agent_id': int(os.environ.get('WECOM_AGENT_ID', '0')),
                'port': int(os.environ.get('PORT', '8000'))
            }
        },
        'llm': {
            'active_model': os.environ.get('LLM_ACTIVE_MODEL', 'gemini'),
            'gemini': {
                'api_key': os.environ.get('GEMINI_API_KEY'),
                'model_name': os.environ.get('GEMINI_MODEL_NAME', 'gemini-1.5-pro')
            },
            'banana': {
                'api_key': os.environ.get('BANANA_API_KEY'),
                'model_key': os.environ.get('BANANA_MODEL_KEY'),
                'url': os.environ.get('BANANA_URL')
            }
        }
    }

def main():
    try:
        config = load_config()
        mode = config['wechat'].get('mode', 'wxauto')
        
        if mode == 'wecom':
            from bot.wecom_bot import WeComBot
            bot = WeComBot(config)
        else:
            from bot.wechat_bot import WeChatBot
            bot = WeChatBot(config)
            
        bot.run()
    except Exception as e:
        logging.error(f"Failed to start bot: {e}")
        # Print full traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
