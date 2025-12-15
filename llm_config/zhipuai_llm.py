from .base_llm import UnifiedLLM
from typing import Any, Dict, List, Optional, Union
from zhipuai import ZhipuAI

class ZhipuAILLM(UnifiedLLM):
    def __init__(self, model: str = "glm-4", api_key: str = None, **kwargs):
        super().__init__(model=model, **kwargs)
        self.client = ZhipuAI(api_key=api_key)

    def call(self, messages: Union[str, List[Dict[str, str]]], tools: Optional[List[dict]] = None, **kwargs) -> Union[str, Any]:
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        return response.choices[0].message.content
