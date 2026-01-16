# broker/ctp_using_working_config.py
import time
from aitrados_api.common_lib.common import load_global_configs
from aitrados_broker.trade_middleware_service.requests import broker_request
from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance
from aitrados_broker.run import run_broker_process
from aitrados_broker.trade_middleware_service.subscriber import AsyncBrokerSubscriber
from aitrados_broker.trade_middleware_service.trade_middleware_identity import broker_identity

class WorkingCTPSubscriber(AsyncBrokerSubscriber):
    """使用成功配置的CTP订阅者"""
    
    def __init__(self):
        super().__init__()
        self.data_received = {
            'account': False,
            'position': False,
            'tick': False,
            'order': False,
            'trade': False
        }
    
    async def on_broker_tick(self, msg):
        self.data_received['tick'] = True
        tick_data = msg["result"]
        print(f"📊 [TICK] {tick_data.get('symbol', 'N/A')}: {tick_data.get('last_price', 'N/A')}")

    async def on_broker_order(self, msg):
        self.data_received['order'] = True
        print(f"📋 [ORDER] {msg.get('result', {})}")

    async def on_broker_trade(self, msg):
        self.data_received['trade'] = True
        print(f"💰 [TRADE] {msg.get('result', {})}")

    async def on_broker_position(self, msg):
        self.data_received['position'] = True
        print(f"📈 [POSITION] {msg.get('result', {})}")

    async def on_broker_account(self, msg):
        self.data_received['account'] = True
        print(f"🏦 [ACCOUNT] {msg.get('result', {})}")

def test_with_working_config():
    """使用成功配置测试"""
    print("🚀 使用成功配置测试CTP连接...")
    
    # 直接使用您直连版本成功使用的配置
    working_config = {
        "provider": "ctp",
        "userid": "240298",  # 使用成功登录的账户
        "password": "19690632Zx!",
        "broker_id": "9999",
        "trade_server": "182.254.243.31:30001",  # 直连版本使用的服务器
        "market_server": "182.254.243.31:30011",
        "product_name": "simnow_client_test",
        "auth_code": "0000000000000000"
    }
    
    print(f"📋 使用工作配置: {working_config['userid']} @ {working_config['trade_server']}")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动中间件和broker
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    time.sleep(3)
    
    # 获取功能类
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    # 设置订阅者
    subscriber = WorkingCTPSubscriber()
    subscriber.run()
    subscriber.subscribe_topics(*broker_identity.channel.get_array())
    
    try:
        print("🔗 开始连接...")
        connect_result = broker_request(fun_cls.CONNECT, setting=working_config)
        print(f"✅ 连接结果: {connect_result}")
        
        print("⏳ 等待认证过程...")
        for i in range(20):
            time.sleep(1)
            print(f"⏰ 等待认证... {i+1}/20")
            
            # 检查数据接收状态
            received_status = [f"{k}:{'✅' if v else '❌'}" for k, v in subscriber.data_received.items()]
            print(f"📊 数据状态: {' '.join(received_status)}")
            
            # 如果收到账户数据，提前退出
            if subscriber.data_received['account']:
                print("✅ 账户数据已到达，认证成功！")
                break
        
        print(f"\n📊 最终数据接收状态:")
        for key, value in subscriber.data_received.items():
            print(f"   {key}: {'✅' if value else '❌'}")
        
        # 尝试获取账户信息
        print("\n🔍 尝试获取账户信息...")
        try:
            accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
            print(f"🏦 账户信息: {accounts}")
        except Exception as e:
            print(f"❌ 获取账户信息失败: {e}")
        
        # 尝试获取持仓信息
        print("\n🔍 尝试获取持仓信息...")
        try:
            positions = broker_request(fun_cls.GET_ALL_POSITIONS)
            print(f"📈 持仓信息: {positions}")
        except Exception as e:
            print(f"❌ 获取持仓信息失败: {e}")
        
        print("\n📡 程序保持运行，接收数据...")
        print("📋 按 Ctrl+C 退出程序")
        
        while True:
            time.sleep(5)
            received_status = [f"{k}:{'✅' if v else '❌'}" for k, v in subscriber.data_received.items()]
            print(f"⏰ 运行中 - 数据状态: {' '.join(received_status)}")
            
    except KeyboardInterrupt:
        print("\n🛑 正在关闭...")
        try:
            broker_request(fun_cls.CLOSE)
        except:
            pass
        print("✅ 程序已退出")

if __name__ == "__main__":
    test_with_working_config()
