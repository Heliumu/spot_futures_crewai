# data_providers/aitrados_data.py
import os
import requests
from datetime import datetime
from typing import List, Optional
from .base import DataProvider
from schemas.models import (
    FuturesHistoryDataPoint,
    PriceDataPoint,
    NewsDataPoint,
    EconomicEvent
)
from dotenv import load_dotenv

load_dotenv()   

class AitradosDataProvider(DataProvider):
    """
    aitrados 数据提供者。
    对接官方 API 获取真实行情、新闻、经济日历等数据。
    """

    def __init__(self):
        self.secret_key = os.getenv("AITRADOS_SECRET_KEY")
        if not self.secret_key:
            raise ValueError("请在 .env 中设置 AITRADOS_SECRET_KEY")
        self.base_url = "https://default.dataset-api.aitrados.com"

    def _build_symbol(self, region: str, ticker: str, contract_type: str = "M1") -> str:
        """
        构建符合 aitrados 规范的 symbol。
        
        Args:
            region: 市场区域 ('cn', 'us', 'global')
            ticker: 商品代码 (如 'rb', 'cu', 'm')
            contract_type: 
                - 'M1' -> 主力连续 (推荐)
                - 'A1' -> 活跃合约
                - 'IDX' -> 指数
                - '2605' -> 具体合约（需传入）
                - '2505!P' -> 历史合约数据
        
        Returns:
            完整 symbol，如 'cn:rb!M1'
        """
        # 转换大小写（ticker 统一小写）
        ticker = ticker.lower()
        
        # 判断是否是具体合约格式（如 RB2605 或 2605）
        if len(ticker) == 6 and ticker.isalnum() and ticker[2:].isdigit():
            # 如 'rb2605' → 直接使用
            full_ticker = ticker.upper()
        elif len(contract_type) == 4 and contract_type.isdigit():  # e.g., "2605"
            full_ticker = f"{ticker.upper()}{contract_type}"
        elif "!" in ticker:
            # 用户已指定完整类型（如 rb!a1）
            full_ticker = ticker.upper()
        else:
            # 默认使用主力连续合约
            valid_types = {"M1", "M2", "A1", "A2", "IDX"}
            if contract_type not in valid_types:
                print(f"⚠️ 未知合约类型 '{contract_type}'。使用默认 M1")
                contract_type = "M1"
            full_ticker = f"{ticker.upper()}!{contract_type}"
        
        return f"{region}:{full_ticker}"

    def get_history_data(
        self,
        asset_class: str,
        region: str,
        ticker: str,
        start_date: Optional[str],
        end_date: Optional[str],
        contract_type: str = "M1"
    ) -> List:
        valid_classes = {"future", "stock", "forex", "crypto"}
        if asset_class not in valid_classes:
            raise ValueError(f"不支持的资产类别: {asset_class}")

        # 构建 symbol，如 cn:RB!A1
        symbol = self._build_symbol(region, ticker, contract_type)
        url = f"{self.base_url}/api/v2/{asset_class}/bars/{symbol}/day/latest"
        params = {
            "secret_key": self.secret_key,
            "format": "json",
            "limit": 140
        }

        try:
            print(f"\n🔍 请求URL: {url}")
            print(f"📡 参数: {params}")

            resp = requests.get(url, params=params, timeout=10)
            print(f"✅ 状态码: {resp.status_code}")

            # 检查是否成功
            if resp.status_code != 200:
                print(f"❌ HTTP 错误: {resp.status_code} - {resp.text}")
                return []

            json_data = resp.json()
            print(f"🎯 JSON keys: {list(json_data.keys())}")  # 应该输出 ['status', 'code', 'result', ...]

            # 🔴 关键修复：真正的数据在 result.data
            if json_data.get("status") != "ok":
                print(f"❌ API 返回错误: {json_data.get('message')}")
                return []

            result_obj = json_data.get("result")
            if not result_obj:
                print("⚠️ 'result' 字段不存在")
                return []

            raw_items = result_obj.get("data", [])
            if not raw_items:
                print("⚠️ 'result.data' 为空，请检查 symbol 是否有效")
                return []

            print(f"✅ 成功获取到 {len(raw_items)} 条原始数据")

            # 开始转换为 FuturesHistoryDataPoint
            result = []
            for item in raw_items:
                try:
                    dt_str = item["datetime"]  # e.g., "2025-06-06T13:00:00+00:00"
                    close_dt_str = item["close_datetime"]

                    # 转换时间格式
                    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
                    close_dt = datetime.fromisoformat(close_dt_str.replace("Z", "+00:00"))

                    data_point = FuturesHistoryDataPoint(
                        datetime=dt,
                        product=ticker.upper(),
                        symbol=item["symbol"],  # 如 RB2605
                        open=float(item["open"]),
                        high=float(item["high"]),
                        low=float(item["low"]),
                        close=float(item["close"]),
                        volume=int(item["volume"]),
                        open_interest=int(item["open_interest"])
                    )
                    result.append(data_point)

                except Exception as e:
                    print(f"⚠️ 跳过一条数据（字段缺失）: {e}")
                    continue

            print(f"✅ 成功解析并返回 {len(result)} 条期货K线数据")
            return result

        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            return []


    def get_news_by_symbol(self, full_symbol: str, limit: int = 5) -> List[NewsDataPoint]:
        url = f"{self.base_url}/api/v2/news/latest"
        params = {
            "secret_key": self.secret_key,
            "full_symbol": full_symbol,
            "limit": limit,
            "format": "json"
        }

        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                print(f"❌ HTTP {resp.status_code}: {resp.text}")
                return []

            json_data = resp.json()
            if json_data.get("status") != "ok":
                print(f"⚠️ API error: {json_data.get('message')}")
                return []

            items = json_data.get("result", {}).get("data", [])
            if not items:
                print("🟡 无相关新闻返回")
                return []

            news_list = []
            for item in items:
                try:
                    # 提取发布时间（兼容多个字段）
                    pub_str = (
                        item.get("published_at") or
                        item.get("pub_time") or
                        item.get("timestamp") or
                        item.get("time") or
                        item.get("created_at")
                    )

                    pub_dt = None
                    if pub_str:
                        clean_str = pub_str.replace("Z", "+00:00")
                        try:
                            pub_dt = datetime.fromisoformat(clean_str)
                        except Exception as e:
                            print(f"时间解析失败: {e}")

                    news_item = NewsDataPoint(
                        id=item.get("id", f"fallback_{len(news_list)}"),
                        title=item["title"],
                        content=item.get("content", "")[:800],
                        source=item.get("source", "Unknown"),
                        published_at=pub_dt,           # 可为 None
                        full_symbol=item.get("full_symbol"),  # 可为 None
                        sentiment_score=item.get("sentiment_score")
                    )
                    news_list.append(news_item)
                except KeyError as e:
                    print(f"缺少必填字段 {e}，跳过一条新闻")
                    continue

            print(f"✅ 成功加载 {len(news_list)} 条新闻")
            return news_list

        except Exception as e:
            print(f"❌ 获取新闻失败: {str(e)}")
            return []



    def get_economic_events(self, days_ahead: int = 7) -> List[EconomicEvent]:
        """获取近期经济日历事件"""
        url = f"{self.base_url}/api/v2/economic_calendar/latest_event_list"
        params = {"secret_key": self.secret_key, "limit": days_ahead}
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            items = resp.json().get("data", [])
            return [
                EconomicEvent(
                    event_id=item["event_id"],
                    event_name=item["event_name"],
                    country=item["country"],
                    importance=item["importance"],
                    actual_value=item.get("actual"),
                    forecast_value=item.get("forecast"),
                    previous_value=item.get("previous"),
                    release_time=datetime.fromisoformat(item["release_time"])
                )
                for item in items
            ]
        except Exception:
            return []
