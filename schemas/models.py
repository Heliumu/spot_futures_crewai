# schemas/models.py

from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional, Generic, TypeVar

# --- API 响应封装器 ---
T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """统一API响应格式"""
    code: int = Field(200, description="状态码")
    message: str = Field("Success", description="响应信息")
    data: List[T] = Field(default_factory=list, description="数据列表")

# --- 具体业务数据模型 ---

class BasisDataPoint(BaseModel):
    """基差数据点"""
    date: date
    product: str
    spot_price: float
    futures_price: float
    basis_value: float = Field(..., description="基差 = 现货价格 - 期货价格")

class PriceDataPoint(BaseModel):
    """通用价格数据点（适用于股票、外汇、加密货币等）"""
    date: date
    product: str = Field(..., description="商品或交易对名称")
    price: float = Field(..., description="收盘价")
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[int] = None
    market: str = Field(..., description="市场标识，如 'cn', 'us', 'global'")

class InventoryDataPoint(BaseModel):
    """库存数据点 (社会/工厂通用)"""
    date: date
    product: str
    inventory_level: float
    location: Optional[str] = Field(None, description="具体地点，如 '主要港口'")
    inventory_type: str = Field(..., description="库存类型，如 '社会库存', '工厂库存'")

class MacroDataPoint(BaseModel):
    """宏观经济数据点"""
    date: date
    indicator_name: str = Field(..., description="指标名称，如 'CPI', 'PMI', 'USD_CNY_RATE'")
    indicator_value: float
    region: str = Field("全国", description="地区，如 '全国', '美国'")

# --- 新增/优化的模型 ---

class FuturesHistoryDataPoint(BaseModel):
    """期货历史K线数据点"""
    datetime: datetime
    product: str
    symbol: str = Field(..., description="合约代码，如 'rb2409'")
    open: float
    high: float
    low: float
    close: float
    volume: int
    open_interest: int

class FuturesSnapshotDataPoint(BaseModel):
    """期货市场快照（主力合约）"""
    product: str
    symbol: str
    last_price: float
    bid_price: float
    ask_price: float
    volume: int
    open_interest: int
    change: float
    change_percent: float

class SupplyDemandDataPoint(BaseModel):
    """行业供需基本面数据点 (替代原来的 FundamentalDataPoint)"""
    date: date
    product: str
    category: str = Field(..., description="大类，如 'Supply', 'Demand', 'Trade'")
    metric: str = Field(..., description="具体指标，如 'Domestic_Production', 'Import_Volume', 'Apparent_Consumption'")
    value: float
    unit: str
    region_or_source: Optional[str] = Field(None, description="地区或来源，如 '全国', '巴西', '饲料行业'")

# 基于aitrados_api 添加的内容
class NewsDataPoint(BaseModel):
    """新闻条目"""
    id: str = Field(..., description="新闻唯一ID")
    title: str = Field(..., description="新闻标题")
    content: str = Field("", description="摘要或全文")
    source: str = Field("Unknown", description="来源媒体")
    
    # ✅ 修改：所有可能为空的字段设为 Optional
    published_at: Optional[datetime] = None
    full_symbol: Optional[str] = None
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0)

class EconomicEvent(BaseModel):
    """经济事件"""
    event_id: str
    event_name: str
    country: str
    importance: int = Field(..., ge=1, le=3)
    actual_value: Optional[str] = None
    forecast_value: Optional[str] = None
    previous_value: Optional[str] = None
    release_time: datetime