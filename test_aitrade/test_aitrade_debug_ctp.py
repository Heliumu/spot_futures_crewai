"""
使用配置管理器测试连接
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trading.trading_manager import trading_manager
from config.trading_config import trading_config

def test_with_config():
    """使用配置管理器测试连接"""
    print("=== 使用配置管理器测试连接 ===")
    
    try:
        # 连接
        success = trading_manager.connect("ctp", "default")
        if success:
            print("✅ 通过配置管理器连接成功!")
            
            # 获取账户信息
            interface = trading_manager.get_interface("ctp")
            account = interface.get_account_info()
            if account:
                print(f"账户ID: {account.accountid}")
                print(f"总资金: {account.balance:.2f}")
                print(f"可用资金: {account.available:.2f}")
            else:
                print("⚠️ 未能获取账户信息")
            
            # 获取持仓信息
            positions = interface.get_positions()
            print(f"持仓数量: {len(positions)}")
            
            # 断开连接
            trading_manager.disconnect()
            print("✅ 测试完成")
            return True
        else:
            print("❌ 连接失败!")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_with_config()
