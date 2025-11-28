# WeChat Bot with LLM Integration

This bot supports two modes:
1. **wxauto**: Controls the WeChat PC Client (Windows only).
2. **WeCom (企业微信)**: Uses the official Enterprise WeChat API (No client needed, runs as a server).

## Prerequisites

1. Python 3.8+
2. **For wxauto mode**: WeChat PC Client installed and logged in.
3. **For WeCom mode**: An Enterprise WeChat account (free to register) and a way to expose your local port to the internet (e.g., ngrok).

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure `config/config.yaml`:
   *   Set `mode` to `"wxauto"` or `"wecom"`.
   *   Fill in the corresponding API keys and settings.

## WeCom Mode Setup (Recommended for Servers/No-Client)

1. Register at [work.weixin.qq.com](https://work.weixin.qq.com/).
2. Create a "Self-built App" (自建应用).
3. Get `CorpID`, `Secret`, `AgentID`.
4. Set `Token` and `EncodingAESKey` in the app settings.
5. **Important**: You need a public URL for the callback.
   *   Use **ngrok** for local testing: `ngrok http 5000`
   *   Set the "URL for Message Receiving" in WeCom to: `https://your-ngrok-url.ngrok-free.app/wechat`

## Usage

Run the bot:
```bash
python main.py
```


