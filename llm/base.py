from abc import ABC, abstractmethod

class LLMBase(ABC):
    @abstractmethod
    def chat(self, prompt: str) -> str:
        """
        Send a prompt to the LLM and get a response.
        """
        pass
