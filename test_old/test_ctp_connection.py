import time
import sys  # 引入sys模块以便必要时强制退出
from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy.trader.object import SubscribeRequest
from vnpy.trader.constant import Exchange
from vnpy_ctp import CtpGateway

# ==================== SimNow 配置 ====================
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

# ==================== 优化后的事件监听器 ====================
def general_event_handler(event: Event):
    # 忽略心跳和通用合约事件，避免刷屏
    if event.type in ["eTimer", "eContract"]:
        return
    
    # 只打印特定合约
    if "Contract" in event.type:
        if "rb2605" in event.data.symbol.lower():
            print(f"  >>> [目标合约] 发现: {event.data.symbol} - {event.data.name}")
        return

    print(f"[事件] 类型: {event.type}")
    
    if "Tick" in event.type:
        print(f"  >>> [行情] 合约:{event.data.symbol} 价格:{event.data.last_price}")
    elif "Log" in event.type:
        print(f"  >>> [日志] {event.data.msg}")

# ==================== 主逻辑 (增加退出清理) ====================
def main():
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    print("主引擎已创建")
    
    main_engine.add_gateway(CtpGateway)
    event_engine.register_general(general_event_handler)
    
    try:
        print("正在连接 CTP 服务器...")
        main_engine.connect(SETTING, "CTP")
        
        print("等待连接和查询合约 (6秒)...")
        time.sleep(6)
        
        # 订阅 rb2605
        symbol = "rb2605"
        req = SubscribeRequest(symbol=symbol, exchange=Exchange.SHFE)
        print(f"正在尝试订阅合约: {symbol} ...")
        main_engine.subscribe(req, "CTP")
        
        print("程序运行中，观察 30 秒...")
        time.sleep(30)
        print("测试观察结束。")

    finally:
        # ==================== 这里的代码是新增的“结束部分” ====================
        print("\n正在清理资源，停止后台线程...")
        
        # 1. 关闭所有网关连接 (断开 CTP)
        main_engine.close()
        
        # 2. 停止事件引擎 (这会终止后台线程，防止程序一直运行)
        event_engine.stop()
        
        print("程序已安全退出。")
        # 如果系统非常顽固，解开下面这行强制退出
        # sys.exit(0)

if __name__ == "__main__":
    main()
