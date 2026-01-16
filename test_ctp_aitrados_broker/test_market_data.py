# focus_on_market_data.py
from aitrados_api.common_lib.common import load_global_configs
from aitrados_api.common_lib.tools.toml_manager import TomlManager
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance

from aitrados_broker import broker_request
from aitrados_broker.run import run_broker_process
from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService
from aitrados_broker.trade_middleware_service.subscriber import AsyncBrokerSubscriber
from aitrados_broker.trade_middleware_service.trade_middleware_identity import broker_identity

class MarketDataSubscriber(AsyncBrokerSubscriber):
    async def on_broker_tick(self, msg):
        print("TICK DATA:", msg["result"])

    async def on_broker_quote(self, msg):
        print("QUOTE DATA:", msg["result"])

load_global_configs(env_file=None, toml_file=None)

if __name__ == "__main__":
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    import time
    time.sleep(3)
    
    # 设置行情数据订阅器
    subscriber = MarketDataSubscriber()
    subscriber.run()
    subscriber.subscribe_topics(*broker_identity.channel.get_array())
    
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    broker_setting = TomlManager.get_value("broker.ctp")
    
    try:
        print("CONNECT", broker_request(fun_cls.CONNECT, setting=broker_setting))
        time.sleep(5)
        
        # 尝试订阅特定合约的行情
        # 你可以先获取可用的合约列表
        print("等待行情数据...")
        
        # 保持运行接收行情数据
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
