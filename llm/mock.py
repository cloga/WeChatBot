from .base import LLMBase

class MockLLM(LLMBase):
    def chat(self, prompt: str) -> str:
        return f"[测试回复] 我收到了你的消息：{prompt}"
