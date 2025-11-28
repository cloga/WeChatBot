import yaml
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_config(path='config/config.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

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
