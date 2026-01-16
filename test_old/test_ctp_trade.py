# test_ctp_fixed.py
import time
from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy.trader.object import (
    OrderRequest,
    CancelRequest,
    SubscribeRequest
)
from vnpy.trader.constant import Exchange, Direction, Offset, OrderType
from vnpy_ctp import CtpGateway

# ==================== 配置 ====================
SETTING = {
    "用户名": "240298",
    "密码": "19690632Zx!",
    "经纪商代码": "9999",
    "交易服务器": "182.254.243.31:30001",
    "行情服务器": "182.254.243.31:30011",
    "产品名称": "simnow_client_test",
    "授权编码": "0000000000000000",
    "柜台环境": "模拟",
}

TEST_SYMBOL = "rb2605"
TEST_EXCHANGE = Exchange.SHFE

def wait_for_data(main_engine, timeout=30):
    """等待账户数据到达"""
    print(f"⏳ 等待账户数据到达，最多等待 {timeout} 秒...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        accounts = main_engine.get_all_accounts()
        if accounts:
            print(f"✅ 账户数据已到达: {len(accounts)} 个账户")
            return accounts[0]  # 返回第一个账户
        
        time.sleep(1)
        print(f"⏰ 等待中... ({int(time.time() - start_time)}s/{timeout}s)")
    
    print("⏰ 账户数据等待超时")
    return None

def main():
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(CtpGateway)
    
    # 事件监听器
    def general_handler(event: Event):
        if event.type == "eLog":
            print(f"[CTP日志] {event.data.msg}")
        elif event.type == "eAccount":
            print(f"[账户数据] {event.data}")
        elif event.type == "ePosition":
            print(f"[持仓数据] {event.data}")
        elif event.type.startswith("eTick"):
            # 只显示特定合约的行情
            if hasattr(event.data, 'symbol') and TEST_SYMBOL in event.data.symbol:
                print(f"[行情] {event.data.symbol}: {event.data.last_price}")
    
    event_engine.register_general(general_handler)

    try:
        print("\n=== 1. 连接网关 ===")
        main_engine.connect(SETTING, "CTP")
        
        print("等待认证完成...")
        time.sleep(10)  # 给更多时间完成认证
        
        print("\n=== 2. 等待账户数据到达 ===")
        account = wait_for_data(main_engine, timeout=60)
        
        if account:
            print(f"✅ 账户余额: {account.available:.2f} (可用), {account.balance:.2f} (总)")
        else:
            print("❌ 无法获取账户信息")
        
        print("\n=== 3. 订阅行情 ===")
        vt_symbol = f"{TEST_SYMBOL}.{TEST_EXCHANGE.value}"
        req = SubscribeRequest(symbol=TEST_SYMBOL, exchange=Exchange.SHFE)
        main_engine.subscribe(req, "CTP")
        
        # 等待行情数据
        print("等待行情数据...")
        for i in range(10):
            time.sleep(1)
            ticks = main_engine.get_tick(vt_symbol)
            if ticks and ticks.last_price:
                print(f"✅ 行情数据: {ticks.symbol} @ {ticks.last_price}")
                break
            print(f"⏰ 等待行情数据... {i+1}/10")
        
        print("\n=== 4. 测试交易功能 ===")
        # 获取最新价格
        ticks = main_engine.get_tick(vt_symbol)
        if ticks and ticks.last_price:
            last_price = ticks.last_price
            limit_price = last_price - 50 
            print(f"最新价: {last_price}, 挂单价: {limit_price}")
            
            # 发送委托单
            order_req = OrderRequest(
                symbol=TEST_SYMBOL,
                exchange=Exchange.SHFE,
                direction=Direction.LONG,
                type=OrderType.LIMIT,
                volume=1,
                price=limit_price,
                offset=Offset.OPEN,
                reference="test_order"
            )
            
            vt_orderid = main_engine.send_order(order_req, "CTP")
            print(f">>> 已发送委托单 ID: {vt_orderid}")
            
            print("等待5秒观察订单状态...")
            time.sleep(5)
            
            # 尝试撤单
            try:
                cancel_req = CancelRequest(
                    orderid=vt_orderid.split('.')[-1],
                    symbol=TEST_SYMBOL,
                    exchange=Exchange.SHFE
                )
                main_engine.cancel_order(cancel_req, "CTP")
                print(">>> 已发送撤单请求")
                time.sleep(3)
            except Exception as e:
                print(f"撤单报错: {e}")
        else:
            print("❌ 无法获取行情数据，跳过交易测试")

    finally:
        print("\n=== 清理退出 ===")
        main_engine.close()
        event_engine.stop()

if __name__ == "__main__":
    main()
