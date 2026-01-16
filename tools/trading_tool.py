"""
AI交易工具 - 支持多平台
"""
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from trading.trading_manager import trading_manager
import os

class TradingInput(BaseModel):
    """交易输入参数"""
    platform: str = Field("ctp", description="交易平台: 'ctp', 'xtp', 'binance' 等")
    action: str = Field(..., description="操作类型: 'buy', 'sell', 'close', 'get_account', 'get_positions'")
    symbol: str = Field("", description="交易代码，如 'rb2409', 'BTCUSDT'")
    volume: int = Field(1, description="交易数量")
    price: float = Field(0.0, description="价格，市价单为0")
    order_type: str = Field("MARKET", description="订单类型: 'MARKET', 'LIMIT'")

class TradingTool(BaseTool):
    """AI交易工具"""
    name: str = "AI Trading Tool"
    description: str = "AI驱动的交易工具，支持多平台交易"
    args_schema: Type[BaseModel] = TradingInput
    
    def _run(self, platform: str, action: str, symbol: str = "", volume: int = 1, 
             price: float = 0.0, order_type: str = "MARKET") -> str:
        """执行交易操作"""
        try:
            interface = trading_manager.get_interface(platform)
            
            # vnpy Direction 枚举映射
            direction_mapping = {
                "buy": "LONG",      # 买多
                "sell": "SHORT",    # 卖空
                "long": "LONG",     # 多头
                "short": "SHORT",   # 空头
                "cover": "LONG",    # 买平（多头）
                "sell_short": "SHORT"  # 卖平（空头）
            }
            
            if action == "buy":
                if not symbol:
                    return "错误: 买入操作需要指定交易代码"
                direction = direction_mapping.get("buy", "LONG")
                orderid = interface.place_order(symbol, direction, volume, price, order_type)
                return f"✅ 买入订单已提交: {symbol} {volume}手, 订单ID: {orderid}"
            
            elif action == "sell":
                if not symbol:
                    return "错误: 卖出操作需要指定交易代码"
                direction = direction_mapping.get("sell", "SHORT")
                orderid = interface.place_order(symbol, direction, volume, price, order_type)
                return f"✅ 卖出订单已提交: {symbol} {volume}手, 订单ID: {orderid}"
            
            elif action == "close":
                if not symbol:
                    return "错误: 平仓操作需要指定交易代码"
                # 根据持仓情况来平仓
                positions = interface.get_positions()
                for pos in positions:
                    if pos.symbol == symbol:
                        # 根据持仓方向决定平仓方向
                        close_direction = "SHORT" if pos.direction == "LONG" else "LONG"
                        orderid = interface.place_order(
                            symbol, close_direction, pos.volume, 0, "MARKET"
                        )
                        return f"✅ 平仓订单已提交: {symbol} {pos.volume}手, 订单ID: {orderid}"
                return f"❌ 未找到 {symbol} 的持仓"
            
            elif action == "get_account":
                account = interface.get_account_info()
                if account:
                    return f"账户信息:\n- 账户ID: {account.accountid}\n- 总资金: {account.balance:.2f}\n- 可用资金: {account.available:.2f}\n- 保证金: {account.margin:.2f}"
                else:
                    return "❌ 无法获取账户信息"
            
            elif action == "get_positions":
                positions = interface.get_positions()
                if positions:
                    result = "持仓信息:\n"
                    for pos in positions:
                        result += f"- {pos.symbol}: {pos.direction} {pos.volume}手 @ {pos.price:.2f}, 盈亏: {pos.pnl:.2f}\n"
                    return result
                else:
                    return "当前无持仓"
            
            else:
                return f"❌ 不支持的操作: {action}"
        
        except Exception as e:
            return f"❌ 操作失败: {str(e)}"
