from .base_llm import UnifiedLLM
from typing import Any, Dict, List, Optional, Union
import dashscope
from dashscope import Generation

class QwenLLM(UnifiedLLM):
    def __init__(self, model: str = "qwen-max", api_key: str = None, **kwargs):
        super().__init__(model=model, **kwargs)
        if api_key:
            dashscope.api_key = api_key

    def call(self, messages: Union[str, List[Dict[str, str]]], tools: Optional[List[dict]] = None, **kwargs) -> Union[str, Any]:
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        response = Generation.call(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            result_format='message'
        )
        if response.status_code == 200:
            return response.output.choices[0].message.content
        else:
            raise RuntimeError(f"DashScope API error: {response.message}")
