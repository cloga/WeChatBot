from flask import Flask, request, abort
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise import parse_message, create_reply
from llm import create_llm
import logging

logger = logging.getLogger(__name__)

class WeComBot:
    def __init__(self, config):
        self.config = config
        self.llm = create_llm(config['llm'])
        
        wecom_conf = config['wechat']['wecom']
        self.token = wecom_conf['token']
        self.encoding_aes_key = wecom_conf['encoding_aes_key']
        self.corp_id = wecom_conf['corp_id']
        self.port = wecom_conf.get('port', 5000)
        
        self.crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        self.app = Flask(__name__)
        
        # Setup routes
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/wechat', methods=['GET', 'POST'])
        def wechat():
            signature = request.args.get('msg_signature', '')
            timestamp = request.args.get('timestamp', '')
            nonce = request.args.get('nonce', '')
            
            if request.method == 'GET':
                echo_str = request.args.get('echostr', '')
                try:
                    echo_str = self.crypto.check_signature(
                        signature,
                        timestamp,
                        nonce,
                        echo_str
                    )
                except InvalidSignatureException:
                    abort(403)
                return echo_str
            
            else:
                try:
                    msg = self.crypto.decrypt_message(
                        request.data,
                        signature,
                        timestamp,
                        nonce
                    )
                except InvalidSignatureException:
                    abort(403)
                
                msg = parse_message(msg)
                if msg.type == 'text':
                    content = msg.content
                    logger.info(f"Received WeCom message: {content}")
                    
                    # 这里可以加入触发词逻辑，或者直接回复
                    # 企业微信应用通常是私聊形式，或者在群里被@
                    
                    reply_content = self.llm.chat(content)
                    
                    reply = create_reply(reply_content, msg)
                    xml = self.crypto.encrypt_message(reply.render(), nonce, timestamp)
                    return xml
                
                return 'success'

    def run(self):
        logger.info(f"Starting WeCom Bot on port {self.port}...")
        self.app.run(host='0.0.0.0', port=self.port)
