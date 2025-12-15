# schemas/models.py

from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional, Generic, TypeVar

# --- API 响应封装器 ---
T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """统一的API响应格式"""
    code: int = Field(200, description="状态码, 200为成功")
    message: str = Field("Success", description="响应信息")
    data: List[T] = Field(..., description="数据列表")

# --- 具体业务数据模型 ---

class BasisDataPoint(BaseModel):
    """基差数据点"""
    date: date
    product: str
    spot_price: float
    futures_price: float
    basis_value: float = Field(..., description="基差 = 现货价格 - 期货价格")

class PriceDataPoint(BaseModel):
    """价格数据点 (现货/期货通用，用于单一价格记录)"""
    date: date
    product: str
    price: float
    market: str = Field(..., description="市场标识，如 '华东现货', 'DCE期货'")

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
    """期货历史K线数据点，用于技术分析"""
    datetime: datetime  # 使用 datetime 以获得更精确的时间
    product: str
    symbol: str = Field(..., description="合约代码，如 'm2501'")
    open: float
    high: float
    low: float
    close: float
    volume: int
    open_interest: int

class FuturesSnapshotDataPoint(BaseModel):
    """期货市场快照数据，用于分析当前状况"""
    product: str
    symbol: str = Field(..., description="主力合约代码")
    last_price: float
    bid_price: float
    ask_price: float
    volume: int
    open_interest: int
    change: float = Field(..., description="涨跌")
    change_percent: float = Field(..., description="涨跌幅(%)")

class SupplyDemandDataPoint(BaseModel):
    """行业供需基本面数据点 (替代原来的 FundamentalDataPoint)"""
    date: date
    product: str
    category: str = Field(..., description="大类，如 'Supply', 'Demand', 'Trade'")
    metric: str = Field(..., description="具体指标，如 'Domestic_Production', 'Import_Volume', 'Apparent_Consumption'")
    value: float
    unit: str
    region_or_source: Optional[str] = Field(None, description="地区或来源，如 '全国', '巴西', '饲料行业'")
