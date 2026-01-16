# test_asphalt_edb.py
from data_providers.ifind_http_client import IFinDHTTPClient
import json

def test_asphalt_edb():
    """测试沥青EDB数据"""
    print("=== 沥青EDB数据测试 ===")
    
    client = IFinDHTTPClient()
    
    # 尝试一些可能的沥青相关指标
    asphalt_indicators = [
        "S5027677",  # 沥青价格指数
        "S5027678",  # 沥青现货价格
        "S5027679",  # 沥青期货价格
        "M0017126",  # 原油价格（相关）
        "S0029692",  # PPMI（相关）
        # 可能需要通过超级命令查询具体指标
    ]
    
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    
    for indicator in asphalt_indicators:
        print(f"\n测试指标: {indicator}")
        try:
            result = client.get_edb_data(
                indicators=[indicator],
                start_date=start_date,
                end_date=end_date
            )
            
            print(f"错误码: {result.get('errorcode', 'N/A')}")
            if result.get('errorcode') == 0:
                print(f"数据长度: {len(result.get('tables', []))}")
                if result.get('tables'):
                    print(f"表格1数据: {result['tables'][0]}")
                break  # 找到一个有效的就停止
            else:
                print(f"错误信息: {result.get('errmsg', 'Unknown')}")
                
        except Exception as e:
            print(f"指标 {indicator} 失败: {e}")

def test_specific_indicators():
    """测试具体指标"""
    print("\n=== 测试具体指标 ===")
    
    client = IFinDHTTPClient()
    
    # 测试一些常见的商品指标
    test_cases = [
        {
            "name": "螺纹钢价格",
            "indicators": ["S5027001"],  # 示例指标
            "start_date": "2024-01-01",
            "end_date": "2024-01-10"
        },
        {
            "name": "原油价格",
            "indicators": ["M0017126"],  # 原油价格指标
            "start_date": "2024-01-01", 
            "end_date": "2024-01-10"
        }
    ]
    
    for case in test_cases:
        print(f"\n测试: {case['name']}")
        try:
            result = client.get_edb_data(
                indicators=case['indicators'],
                start_date=case['start_date'],
                end_date=case['end_date']
            )
            
            print(f"错误码: {result.get('errorcode', 'N/A')}")
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}...")
            
        except Exception as e:
            print(f"失败: {e}")

if __name__ == "__main__":
    test_asphalt_edb()
    test_specific_indicators()
