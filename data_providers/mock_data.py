# data_providers/mock_data.py
import random
from datetime import datetime, date, timedelta
from typing import List, Optional
from .base import DataProvider
from schemas.models import (
    FuturesHistoryDataPoint,
    PriceDataPoint,
    NewsDataPoint,
    EconomicEvent
)

class MockDataProvider(DataProvider):
    """
    模拟数据提供者。
    生成随机但结构正确的数据用于开发和测试。
    """

    def get_history_data(
        self,
        asset_class: str,
        region: str,
        ticker: str,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> List:
        """
        生成模拟的历史行情数据。
        """
        # 解析日期范围
        if start_date:
            try:
                start = date.fromisoformat(start_date)
            except ValueError:
                start = date.today() - timedelta(days=30)
        else:
            start = date.today() - timedelta(days=30)

        if end_date:
            try:
                end = date.fromisoformat(end_date)
            except ValueError:
                end = date.today()
        else:
            end = date.today()

        # 确保开始 <= 结束
        if start > end:
            start, end = end, start

        # 生成数据点列表
        data = []
        current = start
        base_price = 3000.0  # 基础价格

        while current <= end:
            dt = datetime.combine(current, datetime.min.time())
            price_noise = random.uniform(-100, 100)
            open_price = base_price + price_noise
            close_price = base_price + price_noise + random.uniform(-20, 20)
            high_price = max(open_price, close_price) + random.uniform(0, 15)
            low_price = min(open_price, close_price) - random.uniform(0, 15)

            if asset_class == "future":
                item = FuturesHistoryDataPoint(
                    datetime=dt,
                    product=ticker.upper(),
                    symbol=f"{ticker}{current.strftime('%y%m')}",
                    open=open_price,
                    high=high_price,
                    low=low_price,
                    close=close_price,
                    volume=random.randint(8000, 60000),
                    open_interest=random.randint(40000, 200000)
                )
            else:
                item = PriceDataPoint(
                    date=current,
                    product=ticker.upper(),
                    price=close_price,
                    open=open_price,
                    high=high_price,
                    low=low_price,
                    volume=random.randint(1000, 10000),
                    market=f"{region}:{ticker}"
                )
            data.append(item)
            current += timedelta(days=1)

        return data

    def get_news_data(self, query: str, limit: int = 5) -> List[NewsDataPoint]:
        """生成模拟新闻"""
        return [
            NewsDataPoint(
                id=f"mock-news-{i}",
                title=f"【模拟】{query} 行业重大进展",
                content="这是一条由系统生成的模拟新闻内容。",
                source="AI Market News",
                published_at=datetime.now() - timedelta(hours=i*12),
                full_symbol=f"FUTURE:CN:{query.upper()}",
                sentiment_score=random.uniform(-0.5, 0.8)
            )
            for i in range(limit)
        ]

    def get_economic_events(self, days_ahead: int = 7) -> List[EconomicEvent]:
        """生成模拟经济事件"""
        events = ["PMI 发布", "CPI 公布", "利率决议"]
        countries = ["中国", "美国", "欧元区"]
        return [
            EconomicEvent(
                event_id=f"evt-mock-{i}",
                event_name=random.choice(events),
                country=random.choice(countries),
                importance=random.randint(1, 3),
                release_time=datetime.now() + timedelta(days=i, hours=10),
                forecast_value=f"{random.uniform(45, 55):.1f}",
                previous_value=f"{random.uniform(45, 55):.1f}"
            )
            for i in range(days_ahead)
        ]
