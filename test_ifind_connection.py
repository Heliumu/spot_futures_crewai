# test_basic_connection.py
import requests
import os
from datetime import datetime
import dotenv
# 加载环境变量
dotenv.load_dotenv()
def test_basic_connection():
    """测试最基础的连接"""
    print("=== 基础连接测试 ===")
    
    # 获取配置
    access_token = os.getenv("IFIND_ACCESS_TOKEN")
    refresh_token = os.getenv("IFIND_REFRESH_TOKEN")
    base_url = os.getenv("IFIND_BASE_URL", "https://quantapi.51ifind.com/api/v1")
    
    print(f"Access Token: {'已设置' if access_token else '未设置'}")
    print(f"Refresh Token: {'已设置' if refresh_token else '未设置'}")
    print(f"Base URL: {base_url}")
    
    if not access_token:
        print("❌ 请先设置 IFIND_ACCESS_TOKEN 环境变量")
        return
    
    # 1. 测试HTTP连接
    print("\n1. 测试HTTP连接...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"✅ HTTP连接正常 (状态码: {response.status_code})")
    except Exception as e:
        print(f"❌ HTTP连接失败: {e}")
        return
    
    # 2. 测试API端点可用性
    print("\n2. 测试API端点...")
    headers = {
        "Content-Type": "application/json",
        "access_token": access_token
    }
    
    # 尝试发送一个简单的请求来测试token
    test_url = f"{base_url}/basic_data_service"
    test_data = {
        "codes": ["300033.SZ"],
        "indicators": ["ths_close_price_stock"],
        "startdate": "20240101",
        "enddate": "20240102"
    }
    
    try:
        response = requests.post(test_url, json=test_data, headers=headers, timeout=10)
        result = response.json()
        
        print(f"✅ API端点连接正常")
        print(f"   响应状态码: {response.status_code}")
        print(f"   响应内容: {result}")
        
        # 检查错误码
        error_code = result.get('errorcode', 0)
        if error_code == 0:
            print("✅ Token有效，API调用成功")
        elif error_code == -1302:
            print("❌ Token已过期或无效")
        else:
            print(f"⚠️ API返回错误码: {error_code}, 错误信息: {result.get('errmsg')}")
            
    except Exception as e:
        print(f"❌ API调用失败: {e}")
    
    # 3. 如果有refresh_token，测试是否可以用于token刷新
    if refresh_token:
        print("\n3. 检查Refresh Token...")
        print(f"   Refresh Token: {refresh_token[:10]}... (长度: {len(refresh_token)})")
        print("   注意: 需要询问iFinD客服关于token刷新的具体API端点")
    
    print("\n=== 基础连接测试完成 ===")

def get_token_info():
    """分析Token信息"""
    access_token = os.getenv("IFIND_ACCESS_TOKEN")
    if not access_token:
        print("❌ 未设置Access Token")
        return
    
    print("=== Token信息分析 ===")
    print(f"Token长度: {len(access_token)}")
    print(f"Token前缀: {access_token[:20]}...")
    print(f"Token后缀: ...{access_token[-10:]}")
    
    # 尝试解析JWT token（如果适用）
    if '.' in access_token:
        parts = access_token.split('.')
        if len(parts) >= 2:
            import base64
            try:
                # 解码JWT payload
                payload_b64 = parts[1]
                # 补充padding
                payload_b64 += '=' * (4 - len(payload_b64) % 4)
                payload_bytes = base64.b64decode(payload_b64)
                import json
                payload = json.loads(payload_bytes)
                print(f"JWT Payload: {payload}")
            except Exception as e:
                print(f"JWT解析失败: {e}")
    
    print("=== Token信息分析完成 ===")

def main():
    get_token_info()
    test_basic_connection()

if __name__ == "__main__":
    main()
