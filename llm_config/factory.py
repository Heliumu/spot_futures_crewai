# llm_configs/factory.py

import os
import toml
from dotenv import load_dotenv
from .zhipuai_llm import ZhipuAILLM
from .deepseek_llm import DeepSeekLLM
from .qwen_llm import QwenLLM

# 加载 .env 文件中的环境变量
load_dotenv()

# 加载 llms.toml 配置文件
# 假设 factory.py 和 llms.toml 在同一目录下
try:
    with open(os.path.join(os.path.dirname(__file__), 'llms.toml'), 'r', encoding='utf-8') as f:
        llm_configs = toml.load(f)
except FileNotFoundError:
    raise FileNotFoundError("llms.toml configuration file not found in llm_configs directory.")

def get_llm(provider: str, **kwargs):
    """
    根据提供商名称获取一个配置好的 LLM 实例。

    Args:
        provider (str): LLM 提供商名称，如 'zhipuai', 'deepseek', 'qwen'。
        **kwargs: 可选参数，用于在运行时覆盖配置文件中的设置。

    Returns:
        BaseLLM: 一个配置好的 LLM 实例。
    """
    provider_key = provider.lower()
    if provider_key not in llm_configs:
        raise ValueError(f"Unsupported LLM provider: {provider}. Available providers: {list(llm_configs.keys())}")

    # 1. 从 TOML 获取基础配置
    config = llm_configs[provider_key].copy()

    # 2. 从环境变量获取 API Key
    api_key_env_var = f"{provider_key.upper()}_API_KEY"
    api_key = os.getenv(api_key_env_var)
    if not api_key:
        raise ValueError(f"API Key not found in environment variables for {provider}. Please set {api_key_env_var}.")
    config['api_key'] = api_key

    # 3. 用运行时传入的 kwargs 覆盖配置（实现灵活性）
    config.update(kwargs)

    # 4. 根据提供商实例化对应的 LLM
    if provider_key == "zhipuai":
        return ZhipuAILLM(**config)
    elif provider_key == "deepseek":
        return DeepSeekLLM(**config)
    elif provider_key == "qwen":
        return QwenLLM(**config)
    else:
        # 这部分理论上不会执行，因为前面已经检查过
        raise ValueError(f"Unsupported LLM provider: {provider}")

