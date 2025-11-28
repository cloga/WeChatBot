from .gemini import GeminiLLM
from .banana import BananaLLM
from .mock import MockLLM

def create_llm(config):
    active_model = config.get('active_model')
    
    if active_model == 'mock':
        return MockLLM()
    elif active_model == 'gemini':
        conf = config.get('gemini', {})
        return GeminiLLM(
            api_key=conf.get('api_key'),
            model_name=conf.get('model_name')
        )
    elif active_model == 'banana':
        conf = config.get('banana', {})
        return BananaLLM(
            api_key=conf.get('api_key'),
            model_key=conf.get('model_key'),
            url=conf.get('url')
        )
    else:
        raise ValueError(f"Unknown model type: {active_model}")
