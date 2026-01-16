# config/trading_config.py
"""
交易配置管理
"""
import toml
import os
from typing import Dict, Any, Optional
from pathlib import Path

class TradingConfig:
    """交易配置管理器"""
    
    def __init__(self, config_path: str = "config/trading_config.toml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            # 创建默认配置
            self._create_default_config()
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = toml.load(f)
        
        return config
    
    def _create_default_config(self):
        """创建默认配置文件"""
        default_config = {
            "ctp": {
                "username": "240298",
                "password": "19690632Zx!",
                "broker_id": "9999",
                "product_name": "simnow_client_test",
                "auth_code": "0000000000000000",
                "environment": "模拟",
                "trade_server": "182.254.243.31:30001",
                "market_server": "182.254.243.31:30011",
                "accounts": {
                    "default": {
                        "username": "240298",
                        "password": "19690632Zx!",
                        "broker_id": "9999",
                        "enabled": True
                    }
                }
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            toml.dump(default_config, f)
    
    def get_account_config(self, platform: str, account_name: str = "default") -> Dict[str, Any]:
        """获取指定账户的配置"""
        platform_config = self.config.get(platform, {})
        accounts = platform_config.get("accounts", {})
        
        if account_name not in accounts:
            raise ValueError(f"账户 {account_name} 在平台 {platform} 中不存在")
        
        account_config = accounts[account_name].copy()
        
        # 合并平台配置（优先使用账户配置覆盖平台配置）
        platform_defaults = self.config.get(platform, {})
        for key, value in platform_defaults.items():
            if key != "accounts":  # 不合并accounts字段
                if key not in account_config:
                    account_config[key] = value
        
        # 从环境变量获取敏感信息（如果配置中没有）
        if platform == "ctp":
            if "password" not in account_config or not account_config["password"]:
                env_password = os.getenv("CTP_PASSWORD")
                if env_password:
                    account_config["password"] = env_password
        elif platform == "xtp":
            if "api_secret" not in account_config or not account_config["api_secret"]:
                env_secret = os.getenv("XTP_API_SECRET")
                if env_secret:
                    account_config["api_secret"] = env_secret
        elif platform == "binance":
            if "api_secret" not in account_config or not account_config["api_secret"]:
                env_secret = os.getenv("BINANCE_API_SECRET")
                if env_secret:
                    account_config["api_secret"] = env_secret
        
        return account_config
    
    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """获取平台基础配置"""
        return self.config.get(platform, {})
    
    def get_enabled_accounts(self, platform: str) -> Dict[str, Dict[str, Any]]:
        """获取平台所有启用的账户"""
        platform_config = self.config.get(platform, {})
        accounts = platform_config.get("accounts", {})
        
        enabled_accounts = {}
        for name, config in accounts.items():
            if config.get("enabled", False):
                enabled_accounts[name] = config
        
        return enabled_accounts
    
    def add_account(self, platform: str, account_name: str, config: Dict[str, Any]):
        """添加账户配置"""
        if platform not in self.config:
            self.config[platform] = {}
        
        if "accounts" not in self.config[platform]:
            self.config[platform]["accounts"] = {}
        
        self.config[platform]["accounts"][account_name] = config
        self._save_config()
    
    def _save_config(self):
        """保存配置到文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            toml.dump(self.config, f)

# 全局配置实例
trading_config = TradingConfig()
