# test_ctp_trading.py
import time
from aitrados_api.common_lib.common import load_global_configs
from aitrados_api.common_lib.tools.toml_manager import TomlManager

from aitrados_broker.trade_middleware_service.requests import broker_request
from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance
from aitrados_broker.run import run_broker_process
from aitrados_broker.trade_middleware_service.subscriber import AsyncBrokerSubscriber
from aitrados_broker.trade_middleware_service.trade_middleware_identity import broker_identity

class TradingSubscriber(AsyncBrokerSubscriber):
    """交易数据订阅者"""
    
    async def on_broker_tick(self, msg):
        tick_data = msg["result"]
        print(f"【行情】{tick_data.get('symbol', 'N/A')}: "
              f"最新价={tick_data.get('last_price', 'N/A')}, "
              f"买一={tick_data.get('bid_price1', 'N/A')}, "
              f"卖一={tick_data.get('ask_price1', 'N/A')}")

    async def on_broker_order(self, msg):
        order_data = msg["result"]
        print(f"【订单】订单状态更新: {order_data}")

    async def on_broker_trade(self, msg):
        trade_data = msg["result"]
        print(f"【成交】成交记录: {trade_data}")

    async def on_broker_position(self, msg):
        position_data = msg["result"]
        print(f"【持仓】持仓更新: {position_data}")

def trading_example():
    """CTP交易示例"""
    print("启动CTP交易接口...")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动服务
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    # 设置订阅者
    subscriber = TradingSubscriber()
    subscriber.run()
    subscriber.subscribe_topics(*broker_identity.channel.get_array())
    
    time.sleep(3)
    
    # 获取功能类
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    # 连接账户
    broker_setting = TomlManager.get_value("broker.ctp")  # 使用账户1
    print("正在连接CTP账户...")
    
    try:
        connect_result = broker_request(fun_cls.CONNECT, setting=broker_setting)
        print(f"连接结果: {connect_result}")
        
        time.sleep(2)
        
        # 获取基本信息
        accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
        print(f"账户资金: {accounts}")
        
        positions = broker_request(fun_cls.GET_ALL_POSITIONS)
        print(f"持仓情况: {positions}")
        
        # 获取可交易合约
        contracts = broker_request(fun_cls.GET_ALL_CONTRACTS)
        print(f"可交易合约数量: {len(contracts) if contracts else 0}")
        
        print("\nCTP接口运行正常，正在接收实时数据...")
        print("按 Ctrl+C 退出")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n正在关闭连接...")
        try:
            broker_request(fun_cls.CLOSE)
        except:
            pass
        print("程序已退出")

if __name__ == "__main__":
    trading_example()
