# test_ctp_broker_retry.py
import time
import logging
from aitrados_api.common_lib.common import load_global_configs
from aitrados_api.common_lib.tools.toml_manager import TomlManager

from aitrados_broker.trade_middleware_service.requests import broker_request
from aitrados_broker.trade_middleware_service.trade_middleware_rpc_service import AitradosBrokerBackendService
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance
from aitrados_broker.run import run_broker_process
from aitrados_broker.trade_middleware_service.subscriber import AsyncBrokerSubscriber
from aitrados_broker.trade_middleware_service.trade_middleware_identity import broker_identity

class EnhancedCTPSubscriber(AsyncBrokerSubscriber):
    """增强的CTP订阅者类"""
    
    async def on_broker_tick(self, msg):
        tick_data = msg["result"]
        symbol = tick_data.get('symbol', 'N/A')
        last_price = tick_data.get('last_price', 'N/A')
        print(f"📊 [TICK] {symbol}: {last_price}")

    async def on_broker_order(self, msg):
        order_data = msg["result"]
        print(f"📋 [ORDER] {order_data}")

    async def on_broker_trade(self, msg):
        trade_data = msg["result"]
        print(f"💰 [TRADE] {trade_data}")

    async def on_broker_position(self, msg):
        position_data = msg["result"]
        print(f"📈 [POSITION] {position_data}")

    async def on_broker_account(self, msg):
        account_data = msg["result"]
        print(f"🏦 [ACCOUNT] {account_data}")

    async def on_broker_contract(self, msg):
        contract_data = msg["result"]
        if contract_data and len(str(contract_data)) < 200:  # 避免打印过多数据
            print(f"📋 [CONTRACT] {contract_data}")

def wait_for_account_data(max_wait_time=30, check_interval=2):
    """等待账户数据可用"""
    print(f"⏳ 等待账户数据，最多等待 {max_wait_time} 秒...")
    
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        try:
            # 尝试获取账户信息
            accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
            if accounts.get('status') == 'ok' and accounts.get('result'):
                print("✅ 账户数据已就绪")
                return True
            
            # 尝试获取持仓信息
            positions = broker_request(fun_cls.GET_ALL_POSITIONS)
            if positions.get('status') == 'ok' and positions.get('result'):
                print("✅ 持仓数据已就绪")
                return True
                
        except Exception as e:
            print(f"⚠️ 获取账户数据时出错: {e}")
        
        print(f"⏰ 等待中... ({int(time.time() - start_time)}s/{max_wait_time}s)")
        time.sleep(check_interval)
    
    print("⏰ 等待超时，账户数据仍未就绪")
    return False

def enhanced_ctp_example():
    """增强的CTP示例"""
    print("🚀 启动CTP交易接口...")
    
    # 加载配置
    load_global_configs(env_file=None, toml_file=None)
    
    # 启动中间件和broker
    AitradosTradeMiddlewareInstance.run_all()
    run_broker_process(is_thread=True)
    
    # 设置增强的订阅者
    subscriber = EnhancedCTPSubscriber()
    subscriber.run()
    subscriber.subscribe_topics(*broker_identity.channel.get_array())
    
    time.sleep(5)  # 给更多时间让服务启动
    
    # 获取功能类
    fun_cls = AitradosBrokerBackendService.IDENTITY.fun
    
    print("📋 请选择要连接的CTP账户:")
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
        print("❌ 无效选择，使用默认账户1")
        broker_setting = TomlManager.get_value("broker.ctp")
        account_name = "CTP账户1 (252761)"
    
    print(f"\n🔗 正在连接 {account_name}...")
    
    try:
        # 连接
        connect_result = broker_request(fun_cls.CONNECT, setting=broker_setting)
        print(f"✅ 连接结果: {connect_result}")
        
        # 等待一段时间让连接稳定
        print("⏳ 连接建立中，请稍候...")
        time.sleep(10)
        
        # 等待账户数据可用
        if wait_for_account_data(max_wait_time=60, check_interval=3):
            # 获取账户信息
            accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
            print(f"🏦 账户信息: {accounts}")
            
            # 获取持仓信息
            positions = broker_request(fun_cls.GET_ALL_POSITIONS)
            print(f"📈 持仓信息: {positions}")
            
            # 获取合约信息
            contracts = broker_request(fun_cls.GET_ALL_CONTRACTS)
            print(f"📋 合约数量: {len(contracts) if contracts else 0}")
            
            print(f"\n🎉 {account_name} 连接成功并获取到数据！")
        else:
            print(f"\n⚠️ {account_name} 连接成功，但暂时无法获取账户数据")
            print("💡 这可能是由于SimNow认证延迟，请稍后再试")
        
        print("\n📡 程序持续运行，接收实时数据...")
        print("📋 按 Ctrl+C 退出程序")
        
        # 持续监控
        last_check = time.time()
        while True:
            current_time = time.time()
            
            # 每30秒检查一次账户数据
            if current_time - last_check >= 30:
                try:
                    accounts = broker_request(fun_cls.GET_ALL_ACCOUNTS)
                    if accounts.get('status') == 'ok':
                        print(f"🔄 账户数据更新: {accounts.get('result', 'N/A')}")
                except Exception as e:
                    print(f"⚠️ 检查账户数据时出错: {e}")
                
                last_check = current_time
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 正在关闭CTP接口...")
        try:
            broker_request(fun_cls.CLOSE)
        except Exception as e:
            print(f"⚠️ 关闭连接时出错: {e}")
        print("✅ CTP接口已安全关闭")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    enhanced_ctp_example()
