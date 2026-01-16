# broker/ctp_fixed_aitrados.py
import time
from aitrados_api.common_lib.common import load_global_configs
from aitrados_api.common_lib.tools.toml_manager import TomlManager

from aitrados_broker.trade_middleware_service.requests import broker_request
from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance
from aitrados_broker.run import run_broker_process
from aitrados_broker.trade_middleware_service.subscriber import AsyncBrokerSubscriber
from aitrados_broker.trade_middleware_service.trade_middleware_identity import broker_identity

class FixedCTPSubscriber(AsyncBrokerSubscriber):
    """修复的CTP订阅者，用于处理异步数据"""
    
    def __init__(self):
        super().__init__()
        self.account_data = None
        self.position_data = None
        self.account_received = False
        self.position_received = False
        self.tick_received = False
        self.order_received = False
        self.trade_received = False
    
    async def on_broker_tick(self, msg):
        self.tick_received = True
        tick_data = msg["result"]
        print(f"📊 [TICK] {tick_data.get('symbol', 'N/A')}: {tick_data.get('last_price', 'N/A')}")

    async def on_broker_order(self, msg):
        self.order_received = True
        order_data = msg["result"]
        print(f"📋 [ORDER] {order_data}")

    async def on_broker_trade(self, msg):
        self.trade_received = True
        trade_data = msg["result"]
        print(f"💰 [TRADE] {trade_data}")

    async def on_broker_position(self, msg):
        self.position_data = msg["result"]
        self.position_received = True
        print(f"📈 [POSITION] {self.position_data}")

    async def on_broker_account(self, msg):
        self.account_data = msg["result"]
        self.account_received = True
        print(f"🏦 [ACCOUNT] {self.account_data}")

    async def on_broker_contract(self, msg):
        contract_data = msg["result"]
        print(f"📋 [CONTRACT] 收到合约数据: {len(contract_data) if isinstance(contract_data, list) else 'N/A'} 条")

def wait_for_account_data(subscriber, timeout=60):
    """等待账户数据到达"""
    print(f"⏳ 等待账户数据到达，最多等待 {timeout} 秒...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if subscriber.account_received:
            print("✅ 账户数据已到达")
            return True
        time.sleep(1)
        print(f"⏰ 等待中... ({int(time.time() - start_time)}s/{timeout}s)")
    
    print("⏰ 账户数据等待超时")
    return False

def wait_for_position_data(subscriber, timeout=60):
    """等待持仓数据到达"""
    print(f"⏳ 等待持仓数据到达，最多等待 {timeout} 秒...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if subscriber.position_received:
            print("✅ 持仓数据已到达")
            return True
        time.sleep(1)
        print(f"⏰ 等待中... ({int(time.time() - start_time)}s/{timeout}s)")
    
    print("⏰ 持仓数据等待超时")
    return False

def fixed_aitrados_ctp():
    """修复的aitrados CTP示例"""
    print("🚀 启动修复版aitrados CTP交易接口...")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动中间件和broker
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    # 设置修复的订阅者
    subscriber = FixedCTPSubscriber()
    subscriber.run()
    subscriber.subscribe_topics(*broker_identity.channel.get_array())
    
    time.sleep(3)
    
    # 获取功能类
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    # 获取配置并更新服务器地址为成功连接的地址
    broker_setting = TomlManager.get_value("broker.ctp2")
    broker_setting["trade_server"] = "182.254.243.31:30001"
    broker_setting["market_server"] = "182.254.243.31:30011"
    
    print(f"📋 使用配置: {broker_setting['userid']} @ {broker_setting['trade_server']}")
    
    try:
        print("🔗 开始连接CTP...")
        
        # 连接
        connect_result = broker_request(fun_cls.CONNECT, setting=broker_setting)
        print(f"✅ 连接结果: {connect_result}")
        
        # 等待认证完成
        print("⏳ 等待认证完成...")
        time.sleep(15)  # 给足够时间完成认证
        
        # 等待账户数据到达
        print("\n🔍 等待账户数据...")
        account_arrived = wait_for_account_data(subscriber, timeout=60)
        
        if not account_arrived:
            print("⚠️ 账户数据未到达，尝试通过RPC获取...")
        
        # 等待持仓数据到达
        print("\n🔍 等待持仓数据...")
        position_arrived = wait_for_position_data(subscriber, timeout=60)
        
        if not position_arrived:
            print("⚠️ 持仓数据未到达，尝试通过RPC获取...")
        
        # 尝试通过RPC获取数据
        print("\n📊 尝试获取账户数据...")
        try:
            accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
            print(f"🏦 账户信息: {accounts}")
        except Exception as e:
            print(f"❌ 获取账户信息失败: {e}")
        
        print("\n📊 尝试获取持仓数据...")
        try:
            positions = broker_request(fun_cls.GET_ALL_POSITIONS)
            print(f"📈 持仓信息: {positions}")
        except Exception as e:
            print(f"❌ 获取持仓信息失败: {e}")
        
        print("\n📊 尝试获取合约数据...")
        try:
            contracts = broker_request(fun_cls.GET_ALL_CONTRACTS)
            print(f"📋 合约数量: {len(contracts) if contracts else 0}")
        except Exception as e:
            print(f"❌ 获取合约信息失败: {e}")
        
        print(f"\n📡 数据接收状态:")
        print(f"   账户数据到达: {'✅' if subscriber.account_received else '❌'}")
        print(f"   持仓数据到达: {'✅' if subscriber.position_received else '❌'}")
        print(f"   行情数据到达: {'✅' if subscriber.tick_received else '❌'}")
        print(f"   订单数据到达: {'✅' if subscriber.order_received else '❌'}")
        print(f"   成交数据到达: {'✅' if subscriber.trade_received else '❌'}")
        
        print("\n📡 程序保持运行，继续接收数据...")
        print("📋 按 Ctrl+C 退出程序")
        
        # 持续监控
        last_check = time.time()
        while True:
            current_time = time.time()
            
            # 每30秒显示一次状态
            if current_time - last_check >= 30:
                print(f"⏰ 运行中... 账户:{'✅' if subscriber.account_received else '❌'} "
                      f"持仓:{'✅' if subscriber.position_received else '❌'} "
                      f"行情:{'✅' if subscriber.tick_received else '❌'}")
                
                # 再次尝试获取账户数据
                try:
                    accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
                    if accounts.get('status') == 'ok':
                        print(f"🔄 账户数据: {accounts.get('result', 'N/A')}")
                except:
                    pass
                
                last_check = current_time
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 正在关闭...")
        try:
            broker_request(fun_cls.CLOSE)
        except:
            pass
        print("✅ 程序已退出")

if __name__ == "__main__":
    fixed_aitrados_ctp()
