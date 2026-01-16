# broker/ctp_reconnect_example.py
import time
from aitrados_api.common_lib.common import load_global_configs
from aitrados_api.common_lib.tools.toml_manager import TomlManager

from aitrados_broker.trade_middleware_service.requests import broker_request
from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance
from aitrados_broker.run import run_broker_process

def reconnect_ctp():
    """CTP重连示例"""
    print("🔄 CTP重连示例")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动服务
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    time.sleep(3)
    
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    broker_setting = TomlManager.get_value("broker.ctp")
    
    print("🔄 开始连接流程...")
    
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"\n尝试连接 #{retry_count + 1}/{max_retries}")
            
            # 关闭之前的连接（如果存在）
            try:
                broker_request(fun_cls.CLOSE)
                time.sleep(2)
            except:
                pass
            
            # 连接
            connect_result = broker_request(fun_cls.CONNECT, setting=broker_setting)
            print(f"✅ 连接结果: {connect_result}")
            
            if connect_result.get('status') == 'ok':
                print("⏳ 等待认证完成...")
                time.sleep(15)  # 给更多时间认证
                
                # 测试获取数据
                print("🔍 测试数据获取...")
                
                # 尝试获取账户信息
                for i in range(5):
                    time.sleep(3)
                    accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
                    if accounts.get('status') == 'ok':
                        print(f"✅ 账户数据获取成功: {accounts}")
                        return
                    print(f"   尝试 {i+1}/5 获取账户数据...")
                
                print("⚠️ 账户数据仍未就绪，尝试重连...")
            
            retry_count += 1
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            retry_count += 1
            time.sleep(5)
    
    print("❌ 重连失败，已达到最大重试次数")

if __name__ == "__main__":
    reconnect_ctp()
