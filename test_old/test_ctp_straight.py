# fixed_ctp_system.py
"""
修复版CTP交易系统 - 解决认证后数据获取问题
"""

import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy.trader.object import OrderRequest, SubscribeRequest, CancelRequest
from vnpy.trader.constant import Direction, Offset, OrderType, Exchange
from vnpy_ctp import CtpGateway

@dataclass
class AccountInfo:
    """账户信息数据类"""
    accountid: str
    balance: float = 0.0
    available: float = 0.0
    frozen: float = 0.0
    margin: float = 0.0
    close_profit: float = 0.0
    
    @classmethod
    def from_account_data(cls, account_data):
        """从vnpy AccountData创建AccountInfo"""
        return cls(
            accountid=getattr(account_data, 'accountid', 'N/A'),
            balance=getattr(account_data, 'balance', 0.0) or 0.0,
            available=getattr(account_data, 'available', 0.0) or 0.0,
            frozen=getattr(account_data, 'frozen', 0.0) or 0.0,
            margin=getattr(account_data, 'margin', 0.0) or 0.0,
            close_profit=getattr(account_data, 'close_profit', 0.0) or 0.0
        )

@dataclass
class PositionInfo:
    """持仓信息数据类"""
    symbol: str
    direction: str
    volume: int
    available: int
    price: float = 0.0
    pnl: float = 0.0
    
    @classmethod
    def from_position_data(cls, position_data):
        """从vnpy PositionData创建PositionInfo"""
        return cls(
            symbol=position_data.symbol,
            direction=position_data.direction.value,
            volume=position_data.volume,
            available=position_data.available,
            price=getattr(position_data, 'price', 0.0) or 0.0,
            pnl=getattr(position_data, 'pnl', 0.0) or 0.0
        )

class FixedCtpTradingSystem:
    """修复版CTP交易系统"""
    
    def __init__(self):
        self.event_engine = EventEngine()
        self.main_engine = MainEngine(self.event_engine)
        self.main_engine.add_gateway(CtpGateway)
        
        # 事件处理器状态跟踪
        self._account_data = None
        self._positions_data = []
        self._settlement_confirmed = False
        self._first_account_received = False
        self._first_position_received = False
        
        # 注册事件处理器
        self.event_engine.register_general(self._general_handler)
    
    def connect(self, setting: Dict[str, Any], timeout: int = 60) -> bool:
        """
        连接CTP服务器 - 修复版
        """
        print("=== 1. 连接网关 ===")
        self.main_engine.connect(setting, "CTP")
        
        # 等待认证完成
        print(f"等待认证完成 (最多{timeout}秒)...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 检查结算确认状态
            if self._settlement_confirmed:
                print("✅ 认证完成")
                
                # 额外等待数据推送
                print("等待数据推送...")
                time.sleep(3)  # 给数据推送一些时间
                return True
            
            time.sleep(1)
            print(f"⏳ 等待认证... ({int(time.time() - start_time)}s/{timeout}s)")
        
        print("⏰ 认证超时")
        return False
    
    def get_all_accounts(self) -> Optional[List[AccountInfo]]:
        """获取账户信息 - 修复版"""
        try:
            # 首先检查缓存
            if self._account_data:
                return [AccountInfo.from_account_data(self._account_data)]
            
            # 然后调用API
            raw_accounts = self.main_engine.get_all_accounts()
            if not raw_accounts:
                return None
            
            accounts = []
            for acc in raw_accounts:
                accounts.append(AccountInfo.from_account_data(acc))
                # 缓存第一个账户
                if not self._account_data:
                    self._account_data = acc
            return accounts
        except Exception as e:
            print(f"[错误] 获取账户信息失败: {e}")
            return None
    
    def get_all_positions(self) -> Optional[List[PositionInfo]]:
        """获取持仓信息 - 修复版"""
        try:
            # 首先检查缓存
            if self._positions_data:
                positions = []
                for pos in self._positions_data:
                    if getattr(pos, 'volume', 0) > 0:
                        positions.append(PositionInfo.from_position_data(pos))
                return positions
            
            # 然后调用API
            raw_positions = self.main_engine.get_all_positions()
            if not raw_positions:
                return []
            
            positions = []
            for pos in raw_positions:
                if getattr(pos, 'volume', 0) > 0:
                    positions.append(PositionInfo.from_position_data(pos))
                    # 缓存持仓数据
                    if pos not in self._positions_data:
                        self._positions_data.append(pos)
            return positions
        except Exception as e:
            print(f"[错误] 获取持仓信息失败: {e}")
            return []
    
    def _general_handler(self, event: Event):
        """修复版事件处理器"""
        if event.type == "eLog":
            msg = getattr(event.data, 'msg', '')
            print(f"[CTP日志] {msg}")
            
            # 检测结算确认
            if "结算信息确认成功" in msg:
                self._settlement_confirmed = True
                print("[状态] 结算信息确认成功，认证完成")
                
        elif event.type == "eAccount":
            self._account_data = event.data
            self._first_account_received = True
            print(f"[账户更新] {event.data.accountid} - 余额: {getattr(event.data, 'balance', 0.0) or 0.0:.2f}")
            
        elif event.type == "ePosition":
            # 更新持仓缓存
            exists = False
            for i, pos in enumerate(self._positions_data):
                if (pos.symbol == event.data.symbol and 
                    pos.direction == event.data.direction):
                    self._positions_data[i] = event.data  # 更新现有持仓
                    exists = True
                    break
            if not exists:
                self._positions_data.append(event.data)  # 添加新持仓
            
            self._first_position_received = True
            print(f"[持仓更新] {event.data.symbol} {event.data.direction.value} {event.data.volume}手")
            
        elif event.type == "eOrder":
            print(f"[订单状态] {event.data.vt_orderid} -> {event.data.status}")
            
        elif event.type == "eTrade":
            print(f"[成交回报] {event.data.vt_symbol} @ {event.data.price} x {event.data.volume}")
    
    def display_account_info(self):
        """显示账户信息 - 修复版"""
        print("等待账户数据...")
        time.sleep(2)  # 给数据推送时间
        
        accounts = self.get_all_accounts()
        if not accounts:
            print("⚠️ 未获取到账户信息（可能处于非交易时段或数据尚未推送）")
            return
        
        account = accounts[0]
        print("-" * 40)
        print(f"账户ID:     {account.accountid}")
        print(f"总资金:     {account.balance:.2f}")
        print(f"可用资金:   {account.available:.2f}")
        print(f"冻结资金:   {account.frozen:.2f}")
        print(f"保证金:     {account.margin:.2f}")
        print(f"当日盈亏:   {account.close_profit:.2f}")
        print("-" * 40)
    
    def display_position_info(self):
        """显示持仓信息 - 修复版"""
        print("等待持仓数据...")
        time.sleep(2)  # 给数据推送时间
        
        positions = self.get_all_positions()
        if positions is None:
            print("⚠️ 未获取到持仓数据（可能处于非交易时段）")
            return
        elif len(positions) == 0:
            print("当前无持仓。")
            return
        
        print(f"共发现 {len(positions)} 个持仓对象：")
        print("-" * 70)
        print(f"{'合约':<15} {'方向':<6} {'持仓量':<8} {'可平量':<8} {'开仓均价':<10} {'当前盈亏':<10}")
        print("-" * 70)
        
        for pos in positions:
            print(f"{pos.symbol:<15} {pos.direction:<6} {pos.volume:<8} {pos.available:<8} {pos.price:<10.2f} {pos.pnl:<10.2f}")
    
    def close(self):
        """关闭连接"""
        try:
            self.main_engine.close()
        except:
            pass
        try:
            self.event_engine.stop()
        except:
            pass

def main():
    """主函数 - 修复版"""
    # 交易配置
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
    
    trading_system = FixedCtpTradingSystem()
    
    try:
        # 连接
        if not trading_system.connect(SETTING, timeout=60):
            print("❌ 连接失败，请检查配置或网络")
            return
        
        # 显示账户信息
        print("\n=== 账户资金查询 ===")
        trading_system.display_account_info()
        
        # 显示持仓信息
        print("\n=== 持仓查询 ===")
        trading_system.display_position_info()
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n=== 清理退出 ===")
        trading_system.close()

if __name__ == "__main__":
    main()
