"""
修复版CTP连接测试
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trading.interfaces.ctp_interface import CtpInterface

def test_ctp_fixed():
    """修复版CTP连接测试"""
    print("=== 修复版CTP连接测试 ===")
    
    # 准备连接设置
    setting = {
        "用户名": "240298",
        "密码": "19690632Zx!",
        "经纪商代码": "9999",
        "交易服务器": "182.254.243.31:30001",
        "行情服务器": "182.254.243.31:30011",
        "产品名称": "simnow_client_test",
        "授权编码": "0000000000000000",
        "柜台环境": "模拟",
    }
    
    print(f"连接设置: {setting}")
    
    # 创建CTP接口
    ctp_interface = CtpInterface()
    
    try:
        # 连接
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
            print("✅ 测试完成")
            return True
        else:
            print("❌ CTP连接失败!")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_ctp_fixed()
