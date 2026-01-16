# broker/ctp_debug_example.py
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
    """调试用CTP订阅者"""
    
    def __init__(self):
        super().__init__()
        self.data_received = {
            'tick': 0,
            'order': 0,
            'trade': 0,
            'position': 0,
            'account': 0,
            'contract': 0
        }
    
    async def on_broker_tick(self, msg):
        self.data_received['tick'] += 1
        print(f"📊 TICK #{self.data_received['tick']}: {msg.get('result', {}).get('symbol', 'N/A')}")

    async def on_broker_order(self, msg):
        self.data_received['order'] += 1
        print(f"📋 ORDER #{self.data_received['order']}: {msg.get('result', {})}")

    async def on_broker_trade(self, msg):
        self.data_received['trade'] += 1
        print(f"💰 TRADE #{self.data_received['trade']}: {msg.get('result', {})}")

    async def on_broker_position(self, msg):
        self.data_received['position'] += 1
        print(f"📈 POSITION #{self.data_received['position']}: {msg.get('result', {})}")

    async def on_broker_account(self, msg):
        self.data_received['account'] += 1
        print(f"🏦 ACCOUNT #{self.data_received['account']}: {msg.get('result', {})}")

    async def on_broker_contract(self, msg):
        self.data_received['contract'] += 1
        print(f"📋 CONTRACT #{self.data_received['contract']}: {msg.get('result', {})}")

def debug_ctp_connection():
    """调试CTP连接"""
    print("🔧 开始调试CTP连接...")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动中间件和broker
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    # 设置调试订阅者
    subscriber = DebugCTPSubscriber()
    subscriber.run()
    subscriber.subscribe_topics(*broker_identity.channel.get_array())
    
    time.sleep(3)
    
    # 获取功能类
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    # 获取配置
    broker_setting = TomlManager.get_value("broker.ctp")
    print(f"📋 使用配置: {broker_setting}")
    
    print("\n🔗 开始连接CTP账户...")
    
    try:
        # 第一次连接
        print("尝试连接...")
        connect_result = broker_request(fun_cls.CONNECT, setting=broker_setting)
        print(f"✅ 连接结果: {connect_result}")
        
        # 等待更长时间
        print("⏳ 等待认证完成...")
        for i in range(10):
            print(f"⏰ 等待中... {i+1}/10")
            time.sleep(3)
        
        # 分步骤检查
        print("\n🔍 分步骤检查账户状态...")
        
        # 1. 检查连接状态
        print("1. 检查连接状态...")
        try:
            # 先尝试获取合约，这个通常不需要完全认证
            contracts = broker_request(fun_cls.GET_ALL_CONTRACTS)
            print(f"✅ 合约信息: {contracts}")
        except Exception as e:
            print(f"❌ 获取合约失败: {e}")
        
        # 2. 持续检查账户数据
        print("2. 持续检查账户数据...")
        for attempt in range(20):  # 尝试20次
            print(f"   尝试 #{attempt + 1}/20")
            
            # 检查账户
            try:
                accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
                if accounts.get('status') == 'ok':
                    print(f"   ✅ 账户数据获取成功: {accounts}")
                    break
                else:
                    print(f"   ⚠️ 账户数据未就绪: {accounts.get('message', 'Unknown')}")
            except Exception as e:
                print(f"   ❌ 账户请求失败: {e}")
            
            # 检查持仓
            try:
                positions = broker_request(fun_cls.GET_ALL_POSITIONS)
                if positions.get('status') == 'ok':
                    print(f"   ✅ 持仓数据获取成功: {positions}")
                    break
                else:
                    print(f"   ⚠️ 持仓数据未就绪: {positions.get('message', 'Unknown')}")
            except Exception as e:
                print(f"   ❌ 持仓请求失败: {e}")
            
            time.sleep(5)  # 等待5秒再试
        
        print("\n📡 保持连接并监控数据流...")
        print("📊 实时数据统计将显示在上方")
        print("📋 按 Ctrl+C 退出")
        
        # 显示数据统计
        last_stats = dict(subscriber.data_received)
        start_time = time.time()
        
        while True:
            time.sleep(10)
            
            current_time = time.time()
            elapsed = int(current_time - start_time)
            
            current_stats = dict(subscriber.data_received)
            new_data = {k: current_stats[k] - last_stats[k] for k in current_stats}
            
            print(f"⏰ 运行时间: {elapsed}s | 数据统计: "
                  f"Tick:{new_data['tick']} Order:{new_data['order']} "
                  f"Trade:{new_data['trade']} Position:{new_data['position']} "
                  f"Account:{new_data['account']} Contract:{new_data['contract']}")
            
            last_stats = current_stats
            
    except KeyboardInterrupt:
        print("\n🛑 正在关闭...")
        try:
            broker_request(fun_cls.CLOSE)
        except:
            pass
        print("✅ 程序已退出")

if __name__ == "__main__":
    debug_ctp_connection()
