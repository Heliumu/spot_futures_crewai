"""
交易接口抽象基类
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

@dataclass
class TradingAccount:
    """交易账户信息"""
    accountid: str
    balance: float
    available: float
    frozen: float
    margin: float
    close_profit: float

@dataclass
class TradingPosition:
    """持仓信息"""
    symbol: str
    direction: str
    volume: int
    available: int
    price: float
    pnl: float

@dataclass
class TradingOrder:
    """订单信息"""
    symbol: str
    direction: str
    volume: int
    price: float
    order_type: str
    offset: str = "NONE"
    orderid: str = ""

@dataclass
class TradingTick:
    """行情数据"""
    symbol: str
    last_price: float
    volume: int
    open_interest: int
    bid_price: float
    ask_price: float
    datetime: str

class OrderType(Enum):
    """订单类型"""
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    FOK = "FOK"
    FAK = "FAK"

class Direction(Enum):
    """交易方向"""
    BUY = "BUY"
    SELL = "SELL"

class Offset(Enum):
    """开平仓"""
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    CLOSETODAY = "CLOSETODAY"
    CLOSEYESTERDAY = "CLOSEYESTERDAY"

class TradingInterface(ABC):
    """交易接口抽象基类"""
    
    @abstractmethod
    def connect(self, setting: Dict[str, Any]) -> bool:
        """连接交易系统"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass
    
    @abstractmethod
    def get_account_info(self) -> Optional[TradingAccount]:
        """获取账户信息"""
        pass
    
    @abstractmethod
    def get_positions(self) -> List[TradingPosition]:
        """获取持仓信息"""
        pass
    
    @abstractmethod
    def place_order(self, symbol: str, direction: str, volume: int, 
                   price: float, order_type: str = "LIMIT") -> str:
        """下单"""
        pass
    
    @abstractmethod
    def cancel_order(self, orderid: str, symbol: str) -> bool:
        """撤单"""
        pass
    
    @abstractmethod
    def get_order_status(self, orderid: str) -> Optional[TradingOrder]:
        """获取订单状态"""
        pass
    
    @abstractmethod
    def subscribe(self, symbol: str):
        """订阅行情"""
        pass
    
    @abstractmethod
    def get_tick(self, symbol: str) -> Optional[TradingTick]:
        """获取行情"""
        pass
