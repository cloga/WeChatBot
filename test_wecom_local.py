import requests
import yaml
import time
import random
import string
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.enterprise import create_reply, parse_message

def load_config(path='config/config.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_nonce():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

def test_local_wecom():
    # 1. Load Config
    config = load_config()
    wecom_conf = config['wechat']['wecom']
    
    token = wecom_conf['token']
    encoding_aes_key = wecom_conf['encoding_aes_key']
    corp_id = wecom_conf['corp_id']
    port = wecom_conf.get('port', 5000)
    
    print(f"Loaded config. Token: {token}, CorpID: {corp_id}")
    
    # 2. Initialize Crypto
    crypto = WeChatCrypto(token, encoding_aes_key, corp_id)
    
    # 3. Prepare a test message
    test_content = "你好，这是本地测试"
    xml_template = f"""<xml>
    <ToUserName><![CDATA[{corp_id}]]></ToUserName>
    <FromUserName><![CDATA[User123]]></FromUserName>
    <CreateTime>{int(time.time())}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{test_content}]]></Content>
    <MsgId>1234567890123456</MsgId>
    <AgentID>1</AgentID>
    </xml>"""
    
    nonce = generate_nonce()
    timestamp = str(int(time.time()))
    
    # 4. Encrypt the message
    encrypted_xml = crypto.encrypt_message(xml_template, nonce, timestamp)
    
    # Extract the Encrypt content for signature calculation
    # The signature is calculated using the Encrypt field, NOT the full XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(encrypted_xml)
    encrypt_content = root.find('Encrypt').text

    # 5. Generate Signature
    # wechatpy's WeChatCrypto doesn't expose get_signature directly in some versions, 
    # but it uses a standard SHA1 algorithm.
    # signature = sha1(sort(token, timestamp, nonce, encrypt))
    import hashlib
    sort_list = [token, timestamp, nonce, encrypt_content]
    sort_list.sort()
    sha = hashlib.sha1()
    sha.update("".join(sort_list).encode('utf-8'))
    signature = sha.hexdigest()
    
    # 6. Send Request to Local Server
    url = f"http://127.0.0.1:{port}/wechat"
    params = {
        'msg_signature': signature,
        'timestamp': timestamp,
        'nonce': nonce
    }
    
    print(f"\nSending message to {url}...")
    print(f"Content: {test_content}")
    
    try:
        response = requests.post(url, params=params, data=encrypted_xml)
        
        if response.status_code == 200:
            print("\nReceived response from server!")
            # 7. Decrypt Response
            resp_xml = response.content
            
            # The response XML contains the signature, timestamp, and nonce used for the response
            # We need to extract them to verify and decrypt
            import xml.etree.ElementTree as ET
            resp_root = ET.fromstring(resp_xml)
            
            resp_signature = resp_root.find('MsgSignature').text
            resp_timestamp = resp_root.find('TimeStamp').text
            resp_nonce = resp_root.find('Nonce').text
            resp_encrypt = resp_root.find('Encrypt').text
            
            # We can use decrypt_message which verifies the signature internally
            # Note: decrypt_message expects the XML string (or encrypt content), signature, timestamp, nonce
            decrypted_xml = crypto.decrypt_message(resp_xml, resp_signature, resp_timestamp, resp_nonce)
            
            # Parse XML to get content
            # Simple parsing for demonstration
            root = ET.fromstring(decrypted_xml)
            resp_content = root.find('Content').text
            
            print(f"Bot Reply: {resp_content}")
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure 'python main.py' is running in another terminal.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_local_wecom()
