# aitrados_broker_debug.py
"""
aitrados_broker调试版本 - 排除映射问题，专注底层认证流程
"""

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
        self.events_received = []
    
    async def on_broker_tick(self, msg):
        self.events_received.append(('tick', msg))
        print(f"📊 [TICK] {msg.get('result', {}).get('symbol', 'N/A')}")

    async def on_broker_order(self, msg):
        self.events_received.append(('order', msg))
        print(f"📋 [ORDER] {msg.get('result', {})}")

    async def on_broker_trade(self, msg):
        self.events_received.append(('trade', msg))
        print(f"💰 [TRADE] {msg.get('result', {})}")

    async def on_broker_position(self, msg):
        self.events_received.append(('position', msg))
        print(f"📈 [POSITION] {msg.get('result', {})}")

    async def on_broker_account(self, msg):
        self.events_received.append(('account', msg))
        print(f"🏦 [ACCOUNT] {msg.get('result', {})}")

    async def on_broker_log(self, msg):
        """添加日志事件监听"""
        self.events_received.append(('log', msg))
        print(f"[BROKER_LOG] {msg.get('result', {})}")

def debug_aitrados_connection():
    """
    调试aitrados连接 - 使用与直连完全相同的配置格式
    """
    print("🔍 调试aitrados连接...")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动中间件和broker
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    # 设置调试订阅者
    subscriber = DebugCTPSubscriber()
    subscriber.run()
    # 订阅所有频道，包括日志
    subscriber.subscribe_topics(*broker_identity.channel.get_array())
    
    time.sleep(3)
    
    # 获取功能类
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    # 关键：使用与直连版本完全相同的配置格式（中文字段）
    direct_config = {
        "provider": "ctp",
        "用户名": "240298",
        "密码": "19690632Zx!",
        "经纪商代码": "9999",
        "交易服务器": "182.254.243.31:30001",
        "行情服务器": "182.254.243.31:30011",
        "产品名称": "simnow_client_test", 
        "授权编码": "0000000000000000",
        "柜台环境": "模拟"
    }
    
    print("📋 使用与直连完全相同的配置格式")
    
    try:
        print("🔗 开始连接...")
        connect_result = broker_request(fun_cls.CONNECT, setting=direct_config)
        print(f"✅ 连接结果: {connect_result}")
        
        if connect_result.get('status') == 'ok':
            print("⏳ 观察认证过程...")
            
            # 等待足够长时间观察所有事件
            for i in range(60):
                time.sleep(1)
                print(f"⏰ 等待中... {i+1}/60")
                
                # 检查是否收到关键事件
                log_events = [e for e in subscriber.events_received if e[0] == 'log']
                account_events = [e for e in subscriber.events_received if e[0] == 'account']
                
                # 查找结算确认日志
                settlement_confirmed = any(
                    '结算信息确认成功' in str(event[1]) for event in log_events
                )
                
                if settlement_confirmed:
                    print("✅ 结算信息确认成功")
                    
                    # 继续等待账户数据
                    time.sleep(5)
                    accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
                    print(f"📊 账户查询结果: {accounts}")
                    break
                    
        else:
            print("❌ 连接请求失败")
            
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        import traceback
        traceback.print_exc()

def test_original_toml_config():
    """
    测试原始toml配置，但修正服务器地址
    """
    print("\n🔍 测试原始toml配置（修正服务器地址）...")
    
    # 重新初始化
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    time.sleep(3)
    
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    subscriber = DebugCTPSubscriber()
    subscriber.run()
    subscriber.subscribe_topics(*broker_identity.channel.get_array())
    
    # 获取原始配置但修正服务器
    original_config = TomlManager.get_value("broker.ctp")
    original_config["trade_server"] = "182.254.243.31:30001"
    original_config["market_server"] = "182.254.243.31:30011"
    
    print(f"📋 原始配置 (修正服务器): {original_config}")
    
    try:
        connect_result = broker_request(fun_cls.CONNECT, setting=original_config)
        print(f"✅ 连接结果: {connect_result}")
        
        if connect_result.get('status') == 'ok':
            print("⏳ 等待认证...")
            time.sleep(20)
            
            # 检查事件接收情况
            print(f"📊 收到事件总数: {len(subscriber.events_received)}")
            event_types = {}
            for event_type, _ in subscriber.events_received:
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            print(f"事件类型统计: {event_types}")
            
            # 尝试获取账户数据
            accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
            print(f"账户数据: {accounts}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    # 首先测试完全相同的配置格式
    debug_aitrados_connection()
    
    # 然后测试原始配置
    # test_original_toml_config()
