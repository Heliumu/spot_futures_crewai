# test_ctp_single.py
import time
from aitrados_api.common_lib.common import load_global_configs
from aitrados_api.common_lib.tools.toml_manager import TomlManager

from aitrados_broker.trade_middleware_service.requests import broker_request
from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance
from aitrados_broker.run import run_broker_process

def simple_ctp_example():
    """简单的CTP连接示例"""
    print("启动CTP交易接口示例...")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动中间件和broker
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    time.sleep(3)
    
    # 获取功能类
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    # 选择要连接的CTP账户
    print("请选择要连接的CTP账户:")
    print("1. 账户1 (252761)")
    print("2. 账户2 (240298)")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        broker_setting = TomlManager.get_value("broker.ctp")
        account_name = "CTP账户1 (252761)"
    elif choice == "2":
        broker_setting = TomlManager.get_value("broker.ctp2")
        account_name = "CTP账户2 (240298)"
    else:
        print("无效选择，使用默认账户1")
        broker_setting = TomlManager.get_value("broker.ctp")
        account_name = "CTP账户1 (252761)"
    
    print(f"\n正在连接{account_name}...")
    
    try:
        # 连接
        connect_result = broker_request(fun_cls.CONNECT, setting=broker_setting)
        print(f"连接结果: {connect_result}")
        
        time.sleep(2)
        
        # 获取账户信息
        accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
        print(f"账户信息: {accounts}")
        
        # 获取持仓信息
        positions = broker_request(fun_cls.GET_ALL_POSITIONS)
        print(f"持仓信息: {positions}")
        
        print(f"\n{account_name} 连接成功！")
        print("程序持续运行，接收实时数据...")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n正在断开连接...")
        try:
            broker_request(fun_cls.CLOSE)
        except:
            pass
        print("连接已断开")
    except Exception as e:
        print(f"连接失败: {e}")

if __name__ == "__main__":
    simple_ctp_example()
