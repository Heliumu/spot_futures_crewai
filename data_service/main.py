# data_service/main.py
from fastapi import FastAPI, HTTPException, Query
from datetime import date, timedelta
from typing import List, Optional
import random

# 假设 schemas 库已安装或路径可用
from schemas.models import BasisDataPoint, APIResponse, FuturesHistoryDataPoint, MacroDataPoint

app = FastAPI(title="金融数据 API", version="1.0.0")

# --- 模拟数据库 ---
def get_mock_basis_data(product: str, start_date: Optional[date], end_date: Optional[date]) -> List[BasisDataPoint]:
    """生成模拟的基差数据"""
    mock_data = []
    current_date = start_date or date.today() - timedelta(days=30)
    end_date = end_date or date.today()
    
    base_spot = 3000 if product == "豆粕" else 3500
    base_futures = 3050 if product == "豆粕" else 3520

    while current_date <= end_date:
        spot_price = base_spot + random.uniform(-50, 50)
        futures_price = base_futures + random.uniform(-40, 40)
        basis_value = spot_price - futures_price
        mock_data.append(BasisDataPoint(
            date=current_date,
            product=product,
            spot_price=spot_price,
            futures_price=futures_price,
            basis_value=basis_value
        ))
        current_date += timedelta(days=1)
    return mock_data

# --- API 端点 ---
@app.get("/api/v1/data/basis", response_model=APIResponse[BasisDataPoint])
def get_basis_data(
    product: str = Query(..., description="产品名称，如 '沥青'"),
    start_date: Optional[date] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="结束日期 (YYYY-MM-DD)")
):
    """
    获取指定产品的基差数据。
    """
    if not product:
        raise HTTPException(status_code=400, detail="Product name is required.")
        
    data = get_mock_basis_data(product, start_date, end_date)
    
    return APIResponse[BasisDataPoint](
        code=200,
        message=f"Successfully fetched {len(data)} records for {product}.",
        data=data
    )

def get_mock_macro_data(indicator: str, country: str, start_date: Optional[date], end_date: Optional[date]) -> List[MacroDataPoint]:
    # ... 实现宏观数据生成逻辑 ...
    pass

def get_mock_futures_history(product: str, start_date: Optional[date], end_date: Optional[date]) -> List[FuturesHistoryDataPoint]:
    # ... 实现期货历史数据生成逻辑 ...
    pass

# ... 其他模拟函数 ...

# --- API 端点 (新增) ---
@app.get("/api/v1/data/macro", response_model=APIResponse[MacroDataPoint])
def get_macro_data(
    indicator: str = Query(..., description="指标名称"),
    country: str = Query(..., description="国家代码"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None)
):
    data = get_mock_macro_data(indicator, country, start_date, end_date)
    return APIResponse[MacroDataPoint](code=200, message="Success", data=data)

@app.get("/api/v1/data/futures_history", response_model=APIResponse[FuturesHistoryDataPoint])
def get_futures_history_data(
    product: str = Query(...),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None)
):
    data = get_mock_futures_history(product, start_date, end_date)
    return APIResponse[FuturesHistoryDataPoint](code=200, message="Success", data=data)
