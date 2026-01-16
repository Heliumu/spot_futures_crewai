# tools/market_data_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Type
from data_providers import get_data_provider

# 常见 region 白名单（用于警告，非强制）
COMMON_REGIONS = {"cn", "us", "gb", "jp", "de", "fr", "au", "global"}

class MarketDataInput(BaseModel):
    # 统一输入格式
    data_type: str = Field(
        ...,
        description=(
            "数据类型: 'futures_history'（期货K线）, 'news'（相关新闻）"
        )
    )
    asset_class: str = Field(
        ...,
        description="资产类别: 'future', 'stock', 'forex', 'crypto'"
    )
    region: str = Field(
        ...,
        description="市场区域: 'cn', 'us', 'global'"
    )
    ticker: str = Field(
        ...,
        description="交易代码: 'rb', 'cu', 'btcusd'"
    )
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    @field_validator('region')
    def validate_region(cls, v):
        """验证 region 并给出警告"""
        v = v.lower()
        if v not in COMMON_REGIONS:
            print(f"WARNING: 不常见的 region '{v}'. 常见值: {COMMON_REGIONS}")
        return v

class MarketDataTool(BaseTool):
    # ✅ 关键修复：所有字段都必须有类型注解！
    name: str = "Market Data Fetcher"
    description: str = "获取全球多资产市场数据（行情/新闻）"
    args_schema: Type[BaseModel] = MarketDataInput

    def _run(
        self,
        data_type: str,
        asset_class: str,
        region: str,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        provider = get_data_provider()

        try:
            if data_type == "futures_history":
                # 获取历史K线
                data = provider.get_history_data(
                    asset_class=asset_class,
                    region=region,
                    ticker=ticker,
                    start_date=start_date,
                    end_date=end_date
                )
                return f"获取到 {len(data)} 条K线数据。\n最近收盘价: {data[-1].close}"

            elif data_type == "news":
                # ✅ 新增：获取新闻 → 使用 full_symbol 构造规则
                full_symbol = self._build_full_symbol(asset_class, region, ticker)
                news = provider.get_news_by_symbol(full_symbol, limit=5)
                
                if not news:
                    return f"未查到与 {ticker} 相关的新闻。可能该品种暂无报道。"
                
                # 生成简洁摘要
                summary = "\n".join([
                    f"- [{n.published_at.strftime('%Y-%m-%d') if n.published_at else '未知时间'}] "
                    f"{n.title} ({n.source})"
                    for n in news[:3]
                ])
                return f"找到 {len(news)} 条相关资讯（展示前3条）:\n{summary}"

            else:
                return f"不支持的数据类型: {data_type}"

        except Exception as e:
            return f"数据获取失败: {str(e)}。建议使用 WebSearch 工具补充信息。"

    def _build_full_symbol(self, asset_class: str, region: str, ticker: str) -> str:
        """
        根据 aitrados 规范构造 full_symbol。
        示例:
          ('future', 'cn', 'rb') → 'COMMODITY:CN:RB'
          ('crypto', 'global', 'btcusd') → 'CRYPTO:GLOBAL:BTCUSD'
          ('stock', 'us', 'spy') → 'STOCK:US:SPY'
        """
        # 映射 asset_class 到 aitrados 的主类名
        class_map = {
            "future": "COMMODITY",
            "stock": "STOCK",
            "forex": "CURRENCY",
            "crypto": "CRYPTO"
        }
        main_class = class_map.get(asset_class.lower(), "COMMODITY")

        # 转换 region 和 ticker
        region_upper = region.upper()
        ticker_upper = ticker.upper()

        return f"{main_class}:{region_upper}:{ticker_upper}"
