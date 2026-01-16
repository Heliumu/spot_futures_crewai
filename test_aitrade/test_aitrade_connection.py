"""
测试CTP连接
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trading.trading_manager import trading_manager
from config.trading_config import trading_config
from trading.interfaces.ctp_interface import CtpInterface

def test_ctp_connection():
    """测试CTP连接"""
    print("=== 测试CTP连接 ===")
    
    # 获取账户配置
    try:
        account_config = trading_config.get_account_config("ctp", "default")
        print(f"获取到账户配置: {account_config}")
    except Exception as e:
        print(f"获取账户配置失败: {e}")
        return False
    
    # 直接测试CTP接口
    ctp_interface = CtpInterface()
    
    # 准备连接设置
    setting = {
        "用户名": account_config.get("username"),
        "密码": account_config.get("password"),
        "经纪商代码": account_config.get("broker_id", "9999"),
        "交易服务器": account_config.get("trade_server", "182.254.243.31:30001"),
        "行情服务器": account_config.get("market_server", "182.254.243.31:30011"),
        "产品名称": account_config.get("product_name", "simnow_client_test"),
        "授权编码": account_config.get("auth_code", "0000000000000000"),
        "柜台环境": account_config.get("environment", "模拟"),
    }
    
    print(f"连接设置: {setting}")
    
    # 测试连接
    success = ctp_interface.connect(setting)
    
    if success:
        print("✅ CTP连接成功!")
        
        # 获取账户信息
        account = ctp_interface.get_account_info()
        if account:
            print(f"账户ID: {account.accountid}")
            print(f"总资金: {account.balance:.2f}")
            print(f"可用资金: {account.available:.2f}")
        else:
            print("⚠️ 未能获取账户信息")
        
        # 获取持仓信息
        positions = ctp_interface.get_positions()
        print(f"持仓数量: {len(positions)}")
        
        # 断开连接
        ctp_interface.disconnect()
        return True
    else:
        print("❌ CTP连接失败!")
        return False

if __name__ == "__main__":
    test_ctp_connection()
