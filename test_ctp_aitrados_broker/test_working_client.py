# test_working_account.py
import toml
from aitrados_api.common_lib.common import load_global_configs
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance

from aitrados_broker import broker_request
from aitrados_broker.run import run_broker_process
from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService

load_global_configs(env_file=None, toml_file=None)

def convert_ctp_params(ctp_config):
    """转换CTP参数格式"""
    trade_server = ctp_config['trade_server']
    market_server = ctp_config['market_server']
    
    # 确保有tcp://前缀
    if not trade_server.startswith('tcp://'):
        trade_server = f"tcp://{trade_server}"
    if not market_server.startswith('tcp://'):
        market_server = f"tcp://{market_server}"
    
    return {
        "provider": "ctp",
        "用户名": ctp_config.get("userid") or ctp_config.get("username"),  # 支持两种字段名
        "密码": ctp_config["password"],
        "经纪商代码": ctp_config["broker_id"],
        "交易服务器": trade_server,
        "行情服务器": market_server,
        "产品名称": ctp_config["product_name"],
        "授权编码": ctp_config["auth_code"]
    }

if __name__ == "__main__":
    # 手动读取配置文件
    try:
        with open("config.toml", "r", encoding="utf-8") as f:
            config = toml.load(f)
        
        # 使用工作的账户
        ctp_config = config["broker"]["ctp"]
        print("✓ Working account configuration:", ctp_config)
    except Exception as e:
        print(f"✗ Failed to read config.toml: {e}")
        exit(1)
    
    # 转换参数格式
    broker_setting = convert_ctp_params(ctp_config)
    print("✓ Converted config:", broker_setting)
    
    # 启动服务
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    import time
    time.sleep(3)
    
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    try:
        print("Attempting CTP connection with working account...")
        result = broker_request(fun_cls.CONNECT, setting=broker_setting)
        print("CONNECT RESULT:", result)
        
        if result.get('result') is True:
            print("✅ Connection successful!")
            time.sleep(8)  # 等待更长时间
            
            # 获取账户信息
            accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
            print("ACCOUNTS:", accounts)
            
            if accounts.get('status') == 'ok' and accounts.get('result'):
                print("✅ Account data retrieved successfully!")
                
                # 获取其他数据
                positions = broker_request(fun_cls.GET_ALL_POSITIONS)
                print("POSITIONS:", positions)
                
                contracts = broker_request(fun_cls.GET_ALL_CONTRACTS)
                print("CONTRACTS COUNT:", len(contracts.get('result', [])) if contracts.get('result') else 0)
            else:
                print("⚠️ Account data not available")
        else:
            print("❌ Connection failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
