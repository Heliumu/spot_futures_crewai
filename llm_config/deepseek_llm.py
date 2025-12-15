from .base_llm import UnifiedLLM
from typing import Any, Dict, List, Optional, Union
from openai import OpenAI

class DeepSeekLLM(UnifiedLLM):
    def __init__(self, model: str = "deepseek-chat", api_key: str = None, **kwargs):
        super().__init__(model=model, **kwargs)
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def call(self, messages: Union[str, List[Dict[str, str]]], tools: Optional[List[dict]] = None, **kwargs) -> Union[str, Any]:
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        return response.choices[0].message.content
