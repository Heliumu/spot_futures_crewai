# test_complete_ifind.py
from data_providers.ifind_http_client import IFinDHTTPClient, IFinDHTTPDataProvider
from datetime import datetime, timedelta

def test_complete_ifind():
    """测试完整的iFinD功能"""
    print("=== 完整iFinD功能测试 ===")
    
    client = IFinDHTTPClient()
    provider = IFinDHTTPDataProvider()
    
    # 测试日期
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    print(f"测试日期范围: {start_date} 到 {end_date}")
    
    # 1. 测试实时行情
    print("\n1. 测试实时行情...")
    try:
        result = client.get_real_time_quotation(["300033.SZ"])
        print(f"✅ 实时行情获取成功")
        print(f"   错误码: {result.get('errorcode', 'N/A')}")
        if result.get('errorcode') == 0:
            print(f"   数据预览: {str(result)[:300]}...")
    except Exception as e:
        print(f"❌ 实时行情获取失败: {e}")
    
    # 2. 测试历史行情
    print("\n2. 测试历史行情...")
    try:
        result = client.get_history_quotation(
            codes=["300033.SZ"],
            indicators=["open", "high", "low", "close", "volume"],
            start_date=start_date,
            end_date=end_date,
            functionpara={"Fill": "Blank"}
        )
        print(f"✅ 历史行情获取成功")
        print(f"   错误码: {result.get('errorcode', 'N/A')}")
        if result.get('errorcode') == 0:
            print(f"   数据预览: {str(result)[:300]}...")
    except Exception as e:
        print(f"❌ 历史行情获取失败: {e}")
    
    # 3. 测试基础数据
    print("\n3. 测试基础数据...")
    try:
        result = client.get_basic_data(
            codes=["300033.SZ"],
            indipara=[
                {
                    "indicator": "ths_close_price_stock",
                    "indiparams": [start_date.replace("-", ""), end_date.replace("-", "")]
                }
            ],
            start_date=start_date,
            end_date=end_date
        )
        print(f"✅ 基础数据获取成功")
        print(f"   错误码: {result.get('errorcode', 'N/A')}")
        if result.get('errorcode') == 0:
            print(f"   数据预览: {str(result)[:300]}...")
    except Exception as e:
        print(f"❌ 基础数据获取失败: {e}")
    
    # 4. 测试日期序列
    print("\n4. 测试日期序列...")
    try:
        result = client.get_date_sequence(
            codes=["300033.SZ"],
            indipara=[
                {
                    "indicator": "ths_close_price_stock",
                    "indiparams": ["", "100", ""]
                }
            ],
            start_date=start_date,
            end_date=end_date,
            functionpara={"Fill": "Blank"}
        )
        print(f"✅ 日期序列获取成功")
        print(f"   错误码: {result.get('errorcode', 'N/A')}")
        if result.get('errorcode') == 0:
            print(f"   数据预览: {str(result)[:300]}...")
    except Exception as e:
        print(f"❌ 日期序列获取失败: {e}")
    
    # 5. 测试经济数据库
    print("\n5. 测试经济数据库...")
    try:
        # 测试一个常见的经济指标（需要确认具体指标代码）
        result = client.get_edb_data(
            indicators=["G009035746"],  # 示例指标，需要替换为实际指标
            start_date=start_date,
            end_date=end_date
        )
        print(f"✅ 经济数据库获取成功")
        print(f"   错误码: {result.get('errorcode', 'N/A')}")
    except Exception as e:
        print(f"⚠️ 经济数据库获取失败（可能指标不存在）: {e}")
    
    print("\n=== 完整测试完成 ===")

def test_provider_integration():
    """测试数据提供者集成"""
    print("\n=== 数据提供者集成测试 ===")
    
    provider = IFinDHTTPDataProvider()
    
    # 测试股票历史数据
    try:
        result = provider._get_stock_history("300033.SZ", "2024-01-01", "2024-01-10", "cn")
        print(f"✅ 数据提供者股票历史数据获取成功: {len(result)} 条记录")
    except Exception as e:
        print(f"❌ 数据提供者股票历史数据获取失败: {e}")

if __name__ == "__main__":
    test_complete_ifind()
    test_provider_integration()
