"""
CTP交易接口实现
"""
import time
from typing import Dict, List, Optional, Any
import logging

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.object import (
    OrderRequest, SubscribeRequest, CancelRequest,
    AccountData, PositionData, OrderData, TickData
)
from vnpy.trader.constant import Exchange, Direction as VnpyDirection, Offset as VnpyOffset, OrderType as VnpyOrderType
from vnpy_ctp import CtpGateway

from trading.interfaces.trading_interface import (
    TradingInterface, TradingAccount, TradingPosition, TradingOrder, TradingTick,
    Direction, OrderType, Offset
)

logger = logging.getLogger(__name__)

class CtpInterface(TradingInterface):
    """CTP交易接口实现"""
    
    def __init__(self):
        self.event_engine = EventEngine()
        self.main_engine = MainEngine(self.event_engine)
        self.main_engine.add_gateway(CtpGateway)
        
        # 数据缓存
        self.account_data: Optional[TradingAccount] = None
        self.positions: List[TradingPosition] = []
        self.orders: List[OrderData] = []
        self.ticks: Dict[str, TradingTick] = {}
        
        # 注册事件处理器
        self.event_engine.register_general(self._event_handler)
        
        # 是否已连接
        self.connected = False
    
    def _event_handler(self, event):
        """事件处理器"""
        if event.type == "eLog":
            logger.info(f"[CTP LOG] {event.data.msg}")
        elif event.type == "eAccount":
            self.account_data = TradingAccount(
                accountid=event.data.accountid,
                balance=event.data.balance or 0.0,
                available=event.data.available or 0.0,
                frozen=event.data.frozen or 0.0,
                margin=event.data.margin or 0.0,
                close_profit=event.data.close_profit or 0.0
            )
            logger.info(f"[CTP ACCOUNT] 账户数据更新: {event.data.accountid}")
        elif event.type == "ePosition":
            # 更新持仓
            updated = False
            for i, pos in enumerate(self.positions):
                if (pos.symbol == event.data.symbol and 
                    pos.direction == event.data.direction.value):
                    self.positions[i] = TradingPosition(
                        symbol=event.data.symbol,
                        direction=event.data.direction.value,
                        volume=event.data.volume,
                        available=event.data.available,
                        price=event.data.price or 0.0,
                        pnl=event.data.pnl or 0.0
                    )
                    updated = True
                    break
            if not updated:
                self.positions.append(TradingPosition(
                    symbol=event.data.symbol,
                    direction=event.data.direction.value,
                    volume=event.data.volume,
                    available=event.data.available,
                    price=event.data.price or 0.0,
                    pnl=event.data.pnl or 0.0
                ))
            logger.info(f"[CTP POSITION] 持仓更新: {event.data.symbol} {event.data.volume}")
        elif event.type == "eOrder":
            # 订单更新
            updated = False
            for i, order in enumerate(self.orders):
                if order.orderid == event.data.orderid:
                    self.orders[i] = event.data
                    updated = True
                    break
            if not updated:
                self.orders.append(event.data)
            logger.info(f"[CTP ORDER] 订单更新: {event.data.symbol} {event.data.status}")
        elif event.type.startswith("eTick"):
            # 行情更新
            tick_data = event.data
            self.ticks[tick_data.symbol] = TradingTick(
                symbol=tick_data.symbol,
                last_price=tick_data.last_price,
                volume=tick_data.volume,
                open_interest=tick_data.open_interest,
                bid_price=tick_data.bid_price,
                ask_price=tick_data.ask_price,
                datetime=str(tick_data.datetime)
            )
    
    def connect(self, setting: Dict[str, Any]) -> bool:
        """连接CTP"""
        try:
            logger.info("正在连接CTP交易系统...")
            
            # 确保所有必需的参数都存在且为字符串类型
            ctp_setting = {
                "用户名": str(setting.get("username", "")),
                "密码": str(setting.get("password", "")),
                "经纪商代码": str(setting.get("broker_id", "9999")),
                "交易服务器": str(setting.get("trade_server", "182.254.243.31:30001")),
                "行情服务器": str(setting.get("market_server", "182.254.243.31:30011")),
                "产品名称": str(setting.get("product_name", "simnow_client_test")),
                "授权编码": str(setting.get("auth_code", "0000000000000000")),
                "柜台环境": str(setting.get("environment", "模拟")),
            }
            
            # 验证必需参数
            required_fields = ["用户名", "密码", "经纪商代码"]
            for field in required_fields:
                if not ctp_setting[field]:
                    raise ValueError(f"缺少必需的配置参数: {field}")
            
            logger.info(f"准备连接CTP，用户名: {ctp_setting['用户名']}")
            
            # 连接
            self.main_engine.connect(ctp_setting, "CTP")
            
            # 等待连接和认证
            logger.info("等待连接和认证...")
            for i in range(30):  # 等待30秒
                time.sleep(1)
                if self.account_data:  # 如果获取到账户数据，说明认证成功
                    logger.info("✅ CTP认证成功")
                    self.connected = True
                    return True
            
            # 如果30秒后仍未获取到账户数据，尝试手动获取
            logger.info("尝试手动获取账户数据...")
            accounts = self.main_engine.get_all_accounts()
            if accounts:
                account = accounts[0]
                self.account_data = TradingAccount(
                    accountid=account.accountid,
                    balance=account.balance or 0.0,
                    available=account.available or 0.0,
                    frozen=account.frozen or 0.0,
                    margin=account.margin or 0.0,
                    close_profit=account.close_profit or 0.0
                )
                logger.info(f"✅ 手动获取账户数据成功: {self.account_data.accountid}")
                self.connected = True
                return True
            
            logger.warning("⚠️ 连接超时，未能获取账户数据")
            return False
            
        except Exception as e:
            logger.error(f"❌ CTP连接失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def disconnect(self):
        """断开CTP连接"""
        try:
            logger.info("正在断开CTP连接...")
            self.main_engine.close()
            self.event_engine.stop()
            self.connected = False
            logger.info("CTP交易系统已断开")
        except Exception as e:
            logger.error(f"断开CTP连接失败: {e}")
    
    def get_account_info(self) -> Optional[TradingAccount]:
        """获取账户信息"""
        if not self.connected:
            return None
        return self.account_data
    
    def get_positions(self) -> List[TradingPosition]:
        """获取持仓信息"""
        if not self.connected:
            return []
        return self.positions.copy()
    
    def place_order(self, symbol: str, direction: str, volume: int, 
                   price: float, order_type: str = "LIMIT") -> str:
        """下单"""
        if not self.connected:
            raise Exception("交易系统未连接")
        
        try:
            # 转换方向
            direction_enum = VnpyDirection(direction)
            
            # 转换订单类型
            order_type_enum = VnpyOrderType(order_type)
            
            req = OrderRequest(
                symbol=symbol,
                exchange=Exchange.SHFE,  # 根据实际交易所调整
                direction=direction_enum,
                type=order_type_enum,
                volume=volume,
                price=price,
                offset=VnpyOffset.NONE
            )
            
            orderid = self.main_engine.send_order(req, "CTP")
            logger.info(f"✅ CTP订单已发送: {symbol} {direction} {volume}手 @ {price}")
            return orderid
            
        except Exception as e:
            logger.error(f"❌ CTP下单失败: {e}")
            raise e
    
    def cancel_order(self, orderid: str, symbol: str) -> bool:
        """撤单"""
        try:
            req = CancelRequest(
                orderid=orderid,
                symbol=symbol,
                exchange=Exchange.SHFE
            )
            result = self.main_engine.cancel_order(req, "CTP")
            logger.info(f"✅ CTP撤单请求已发送: {orderid}")
            return result
        except Exception as e:
            logger.error(f"❌ CTP撤单失败: {e}")
            return False
    
    def get_order_status(self, orderid: str) -> Optional[TradingOrder]:
        """获取订单状态"""
        for order in self.orders:
            if order.orderid == orderid:
                return TradingOrder(
                    symbol=order.symbol,
                    direction=order.direction.value,
                    volume=order.volume,
                    price=order.price,
                    order_type=order.type.value,
                    offset=order.offset.value,
                    orderid=order.orderid
                )
        return None
    
    def subscribe(self, symbol: str):
        """订阅行情"""
        try:
            req = SubscribeRequest(
                symbol=symbol,
                exchange=Exchange.SHFE
            )
            self.main_engine.subscribe(req, "CTP")
            logger.info(f"✅ CTP订阅行情: {symbol}")
        except Exception as e:
            logger.error(f"❌ CTP订阅行情失败: {e}")
    
    def get_tick(self, symbol: str) -> Optional[TradingTick]:
        """获取行情"""
        return self.ticks.get(symbol)
