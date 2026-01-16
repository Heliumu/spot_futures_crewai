# llm_config/base_llm.py
from crewai import BaseLLM
from typing import Any, Dict, List, Optional, Union

class UnifiedLLM(BaseLLM):
    """统一封装基类，所有自定义LLM建议继承此类，便于扩展。"""

    def __init__(self, model: str, temperature: Optional[float] = None, **kwargs):
        super().__init__(model=model, temperature=temperature)
        self.extra_params = kwargs

    def supports_function_calling(self) -> bool:
        return True

    def supports_stop_words(self) -> bool:
        return True

    def get_context_window_size(self) -> int:
        return 8192
