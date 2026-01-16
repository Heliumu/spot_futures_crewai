# broker/debug_ctp_auth.py
import time
from aitrados_api.common_lib.common import load_global_configs
from aitrados_api.common_lib.tools.toml_manager import TomlManager

from aitrados_broker.trade_middleware_service.requests import broker_request
from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance
from aitrados_broker.run import run_broker_process
from aitrados_broker.trade_middleware_service.subscriber import AsyncBrokerSubscriber
from aitrados_broker.trade_middleware_service.trade_middleware_identity import broker_identity

class DebugCTPSubscriber(AsyncBrokerSubscriber):
    """调试CTP订阅者"""
    
    def __init__(self):
        super().__init__()
        self.events_received = []
    
    async def on_broker_tick(self, msg):
        print(f"📊 [TICK] {msg.get('result', {})}")
        self.events_received.append(('tick', msg))

    async def on_broker_order(self, msg):
        print(f"📋 [ORDER] {msg.get('result', {})}")
        self.events_received.append(('order', msg))

    async def on_broker_trade(self, msg):
        print(f"💰 [TRADE] {msg.get('result', {})}")
        self.events_received.append(('trade', msg))

    async def on_broker_position(self, msg):
        print(f"📈 [POSITION] {msg.get('result', {})}")
        self.events_received.append(('position', msg))

    async def on_broker_account(self, msg):
        print(f"🏦 [ACCOUNT] {msg.get('result', {})}")
        self.events_received.append(('account', msg))

    async def on_broker_contract(self, msg):
        print(f"📋 [CONTRACT] {len(msg.get('result', [])) if isinstance(msg.get('result', []), list) else 'N/A'} 条")
        self.events_received.append(('contract', msg))

def test_different_configs():
    """测试不同的配置组合"""
    print("🔧 开始测试不同的配置组合...")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动中间件和broker
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    time.sleep(3)
    
    # 获取功能类
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    # 测试配置组合
    test_configs = [
        {
            "name": "原配置1 (252761)",
            "config": TomlManager.get_value("broker.ctp")
        },
        {
            "name": "原配置2 (240298)", 
            "config": TomlManager.get_value("broker.ctp2")
        },
        {
            "name": "配置1 + 直连服务器",
            "config": {**TomlManager.get_value("broker.ctp"), 
                      "trade_server": "182.254.243.31:30001",
                      "market_server": "182.254.243.31:30011"}
        },
        {
            "name": "配置2 + 直连服务器",
            "config": {**TomlManager.get_value("broker.ctp2"), 
                      "trade_server": "182.254.243.31:30001",
                      "market_server": "182.254.243.31:30011"}
        }
    ]
    
    for test_config in test_configs:
        print(f"\n{'='*50}")
        print(f"测试配置: {test_config['name']}")
        print(f"账户: {test_config['config']['userid']}")
        print(f"交易服务器: {test_config['config']['trade_server']}")
        print(f"行情服务器: {test_config['config']['market_server']}")
        print(f"{'='*50}")
        
        # 设置订阅者
        subscriber = DebugCTPSubscriber()
        subscriber.run()
        subscriber.subscribe_topics(*broker_identity.channel.get_array())
        
        try:
            print(f"🔗 尝试连接...")
            connect_result = broker_request(fun_cls.CONNECT, setting=test_config['config'])
            print(f"✅ 连接结果: {connect_result}")
            
            print("⏳ 观察认证过程...")
            time.sleep(10)  # 给足够时间观察认证过程
            
            # 检查是否收到账户数据
            account_found = any(event[0] == 'account' for event in subscriber.events_received)
            if account_found:
                print("✅ 收到账户数据")
            else:
                print("❌ 未收到账户数据")
            
            print(f"📊 总共收到事件: {len(subscriber.events_received)} 个")
            
            # 关闭连接
            try:
                broker_request(fun_cls.CLOSE)
                time.sleep(2)
            except:
                pass
                
        except Exception as e:
            print(f"❌ 连接失败: {e}")
        
        print(f"继续下一个配置测试...")
        time.sleep(5)

def debug_single_config():
    """调试单个配置"""
    print("🔧 调试单个配置...")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动中间件和broker
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    time.sleep(3)
    
    # 获取功能类
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    # 获取配置
    broker_setting = TomlManager.get_value("broker.ctp")
    
    # 打印配置详情
    print(f"📋 配置详情:")
    for key, value in broker_setting.items():
        print(f"   {key}: {value}")
    
    # 设置订阅者
    subscriber = DebugCTPSubscriber()
    subscriber.run()
    subscriber.subscribe_topics(*broker_identity.channel.get_array())
    
    try:
        print("\n🔗 开始连接...")
        connect_result = broker_request(fun_cls.CONNECT, setting=broker_setting)
        print(f"✅ 连接请求结果: {connect_result}")
        
        print("⏳ 详细观察认证过程...")
        for i in range(15):
            time.sleep(1)
            print(f"⏰ 等待认证... {i+1}/15")
            
            # 检查是否收到账户数据
            account_found = any(event[0] == 'account' for event in subscriber.events_received)
            if account_found:
                print("✅ 账户数据已到达")
                break
                
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🔍 CTP认证调试工具")
    print("1. 测试所有配置组合")
    print("2. 调试单个配置")
    
    choice = input("请选择 (1 或 2): ").strip()
    
    if choice == "1":
        test_different_configs()
    elif choice == "2":
        debug_single_config()
    else:
        print("无效选择，运行单个配置调试")
        debug_single_config()

if __name__ == "__main__":
    main()
