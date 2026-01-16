
import time
from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
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

def main():
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(CtpGateway)
    
    # 打印关键日志
    def general_handler(event: Event):
        if event.type == "eLog":
            print(f"[CTP日志] {event.data.msg}")
            
    event_engine.register_general(general_handler)

    try:
        print("\n=== 1. 连接网关 ===")
        main_engine.connect(SETTING, "CTP")
        
        # 登录后，VeighNa 会自动查询一次账户和持仓，我们需要给点时间等待回报
        print("正在查询账户和持仓数据 (等待 8 秒)...")
        time.sleep(30)

        print("\n=== 2. 账户资金查询 ===")
        # 获取所有账户信息
        accounts = main_engine.get_all_accounts()
        
        if not accounts:
            print("❌ 未获取到账户信息！可能是连接未完全建立或查询失败。")
        else:
            account = accounts[0]
            print("-" * 30)
            print(f"账户ID:     {account.accountid}")
            print(f"总资金:     {account.balance:.2f}")      # 总权益
            print(f"可用资金:   {account.available:.2f}")    # 可用于开仓的资金
            print(f"冻结资金:   {account.frozen:.2f}")      # 挂单冻结
            print(f"保证金:     {account.margin:.2f}")      # 占用保证金
            print(f"当日盈亏:   {account.close_profit:.2f}") # CTP通常为0，直到日结
            print("-" * 30)

        print("\n=== 3. 持仓查询 ===")
        # 获取所有持仓
        positions = main_engine.get_all_positions()
        
        if not positions:
            print("当前无持仓。")
        else:
            print(f"共发现 {len(positions)} 个持仓对象：")
            print("-" * 60)
            print(f"{'合约':<15} {'方向':<6} {'持仓量':<8} {'可平量':<8} {'开仓均价':<10} {'当前盈亏':<10}")
            print("-" * 60)
            
            for pos in positions:
                # 过滤掉持仓量为0的无效数据
                if pos.volume == 0:
                    continue
                
                print(f"{pos.symbol:<15} {pos.direction.value:<6} {pos.volume:<8} {pos.available:<8} {pos.price:<10.2f} {pos.pnl:<10.2f}")

    finally:
        print("\n=== 清理退出 ===")
        main_engine.close()
        event_engine.stop()

if __name__ == "__main__":
    main()
