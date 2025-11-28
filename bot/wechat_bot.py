from wxauto import WeChat
from llm import create_llm
import logging
import time

logger = logging.getLogger(__name__)

class WeChatBot:
    def __init__(self, config):
        self.config = config
        self.llm = create_llm(config['llm'])
        self.wx = WeChat()
        
        # 获取当前登录账号信息（可选，用于日志）
        try:
            self.nickname = self.wx.nickname
            logger.info(f"WeChat initialized. Logged in as: {self.nickname}")
        except:
            logger.warning("Could not retrieve nickname. Make sure WeChat is running and logged in.")

    def process_messages(self):
        # 获取监听列表中的新消息
        # wxauto 的 GetListenMessage 返回的是一个字典: {chat_name: [msg_obj, ...]}
        msgs = self.wx.GetListenMessage()
        
        for chat_name, msg_list in msgs.items():
            for msg in msg_list:
                # 过滤掉自己发送的消息
                if msg.type == 'sys':
                    continue
                    
                content = msg.content
                sender_name = msg.sender # 发送者昵称
                
                # 处理群聊消息
                # wxauto 并没有直接的 isGroup 属性，通常通过 chat_name 是否在通讯录或者消息特征判断
                # 这里简单处理：如果消息内容包含 @我，或者是在已知的群里
                
                # 简单的 @机器人 逻辑
                # 注意：wxauto 获取的 content 包含 @文本
                
                # 检查触发词
                # 优先使用配置文件中的 trigger_word，如果没有配置，则默认使用 @昵称
                trigger_word = self.config['wechat'].get('trigger_word')
                
                if not trigger_word:
                    # 如果没配置 trigger_word，尝试使用昵称
                    name_to_use = self.config['wechat'].get('bot_name', self.nickname)
                    trigger_word = f"@{name_to_use}"
                
                is_at_me = trigger_word in content
                
                if is_at_me:
                    # 群聊 @ 回复
                    logger.info(f"Received trigger '{trigger_word}' from {chat_name} - {sender_name}: {content}")
                    
                    # 去掉触发词部分
                    clean_content = content.replace(trigger_word, "").strip()
                    
                    # 调用 LLM
                    reply = self.llm.chat(clean_content)
                    
                    # 回复 (wxauto 会自动发送到当前 chat_name)
                    # SendMsg(msg, who=chat_name)
                    # 为了确保回复给正确的人，最好加上 @sender_name
                    final_reply = f"@{sender_name} {reply}"
                    self.wx.SendMsg(final_reply, who=chat_name)
                    
                elif chat_name != bot_name: 
                    # 私聊 (假设 chat_name 就是好友名字，且不是自己)
                    # 这里需要更严谨的判断，比如配置允许私聊的好友列表，或者默认不回私聊以免打扰
                    # 简单起见，这里只回私聊（非群聊逻辑比较难判断，wxauto视所有会话为同类）
                    
                    # 策略：如果不是 @ 消息，且是私聊（通常私聊不会有 @），则回复
                    # 但为了防止群聊里的普通消息也被回复，我们需要区分。
                    # wxauto 比较难区分群和好友，除非维护一个列表。
                    # 暂时策略：只回复包含特定前缀的消息，或者只回复 @ 消息
                    pass

    def run(self):
        logger.info("Bot started. Listening for messages...")
        # 添加监听对象（可选，如果不加，默认监听所有新消息，但最好手动把群加入监听列表）
        # self.wx.AddListenChat(who='群名') 
        
        while True:
            try:
                self.process_messages()
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Bot stopped.")
                break
            except Exception as e:
                logger.error(f"Error in loop: {e}")
                time.sleep(2)

