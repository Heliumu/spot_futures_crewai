"""
配置调试测试
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.trading_config import trading_config
from trading.interfaces.ctp_interface import CtpInterface

def test_config():
    """测试配置获取"""
    print("=== 配置获取测试 ===")
    
    try:
        # 获取账户配置
        account_config = trading_config.get_account_config("ctp", "default")
        print(f"获取到账户配置: {account_config}")
        
        # 检查必需字段
        required_fields = ["username", "password", "broker_id"]
        for field in required_fields:
            value = account_config.get(field)
            print(f"{field}: {value} (类型: {type(value)})")
            if not value:
                print(f"❌ {field} 为空或不存在")
            else:
                print(f"✅ {field} 存在")
        
        # 检查vnpy需要的字段名
        ctp_setting = {
            "用户名": str(account_config.get("username", "")),
            "密码": str(account_config.get("password", "")),
            "经纪商代码": str(account_config.get("broker_id", "9999")),
            "交易服务器": str(account_config.get("trade_server", "182.254.243.31:30001")),
            "行情服务器": str(account_config.get("market_server", "182.254.243.31:30011")),
            "产品名称": str(account_config.get("product_name", "simnow_client_test")),
            "授权编码": str(account_config.get("auth_code", "0000000000000000")),
            "柜台环境": str(account_config.get("environment", "模拟")),
        }
        
        print(f"\n转换后的CTP设置: {ctp_setting}")
        
        # 检查vnpy字段
        for field in ["用户名", "密码", "经纪商代码"]:
            value = ctp_setting[field]
            print(f"vnpy {field}: '{value}' (类型: {type(value)}, 长度: {len(value) if value else 0})")
            if not value or len(str(value)) == 0:
                print(f"❌ vnpy {field} 为空")
            else:
                print(f"✅ vnpy {field} 存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置获取失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ctp_direct():
    """直接测试CTP接口"""
    print("\n=== 直接CTP接口测试 ===")
    
    # 使用硬编码的配置进行测试
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
    
    print(f"直接使用设置: {setting}")
    
    ctp_interface = CtpInterface()
    
    try:
        success = ctp_interface.connect(setting)
        if success:
            print("✅ 直接连接成功!")
            account = ctp_interface.get_account_info()
            if account:
                print(f"账户ID: {account.accountid}")
                print(f"总资金: {account.balance:.2f}")
            else:
                print("⚠️ 未能获取账户信息")
        else:
            print("❌ 直接连接失败!")
        
        ctp_interface.disconnect()
        return success
    except Exception as e:
        print(f"❌ 直接连接失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_config()
    test_ctp_direct()
