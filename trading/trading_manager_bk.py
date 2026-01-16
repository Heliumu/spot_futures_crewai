"""
交易系统管理器 - 统一管理多平台交易接口
"""
from typing import Dict, Optional, Any, List
from trading.interfaces.trading_interface import TradingInterface
from trading.interfaces.ctp_interface import CtpInterface
from config.trading_config import trading_config

class TradingManager:
    """交易系统管理器"""
    
    def __init__(self):
        self.interfaces: Dict[str, TradingInterface] = {}
        self.current_interface: Optional[TradingInterface] = None
        self.current_platform: str = ""
        self.current_account: str = ""
    
    def register_interface(self, platform: str, interface: TradingInterface):
        """注册交易接口"""
        self.interfaces[platform.lower()] = interface
    
    def connect(self, platform: str, account_name: str = "default") -> bool:
        """连接指定平台的指定账户"""
        platform = platform.lower()
        if platform not in self.interfaces:
            raise ValueError(f"不支持的交易平台: {platform}")
        
        # 获取账户配置
        account_config = trading_config.get_account_config(platform, account_name)
        
        # 合并平台配置和账户配置
        platform_config = trading_config.get_platform_config(platform)
        setting = {**platform_config, **account_config}
        
        interface = self.interfaces[platform]
        success = interface.connect(setting)
        
        if success:
            self.current_interface = interface
            self.current_platform = platform
            self.current_account = account_name
            return True
        return False
    
    def connect_multiple_accounts(self, connections: Dict[str, Dict[str, str]]) -> Dict[str, bool]:
        """连接多个账户
        connections: {
            "ctp_account_1": {"platform": "ctp", "account": "account_1"},
            "xtp_account_1": {"platform": "xtp", "account": "xtp_paper"}
        }
        """
        results = {}
        for conn_name, conn_info in connections.items():
            try:
                platform = conn_info["platform"]
                account = conn_info["account"]
                success = self.connect(platform, account)
                results[conn_name] = success
            except Exception as e:
                results[conn_name] = False
                print(f"连接 {conn_name} 失败: {e}")
        
        return results
    
    def disconnect(self):
        """断开当前连接"""
        if self.current_interface:
            self.current_interface.disconnect()
            self.current_interface = None
            self.current_platform = ""
            self.current_account = ""
    
    def get_interface(self, platform: Optional[str] = None) -> TradingInterface:
        """获取指定平台的接口"""
        if platform:
            platform = platform.lower()
            if platform in self.interfaces:
                return self.interfaces[platform]
        else:
            if self.current_interface:
                return self.current_interface
        
        raise ValueError(f"未找到平台 {platform} 的接口")
    
    def get_available_platforms(self) -> List[str]:
        """获取可用平台列表"""
        return list(self.interfaces.keys())

# 全局交易管理器实例
trading_manager = TradingManager()

# 注册CTP接口
trading_manager.register_interface("ctp", CtpInterface())
