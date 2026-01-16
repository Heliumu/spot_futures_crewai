# test_ifind_direct.py
import requests
import os
from datetime import datetime
import dotenv

# 加载环境变量
dotenv.load_dotenv()

def test_direct_connection():
    """直接测试连接"""
    print("=== 直接连接测试 ===")
    
    access_token = os.getenv("IFIND_ACCESS_TOKEN")
    base_url = os.getenv("IFIND_BASE_URL", "https://quantapi.51ifind.com/api/v1")
    
    print(f"Access Token: {access_token[:10]}...")
    print(f"Base URL: {base_url}")
    
    # 尝试不同的header格式
    header_options = [
        # 选项1: 使用access_token作为header
        {"Content-Type": "application/json", "access_token": access_token},
        # 选项2: 使用Authorization header
        {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
        # 选项3: 使用Token作为URL参数
        {"Content-Type": "application/json"},
    ]
    
    test_data = {
        "codes": ["300033.SZ"],
        "indicators": ["ths_latest_price_stock"],
        "startdate": "20240101",
        "enddate": "20240102"
    }
    
    for i, headers in enumerate(header_options):
        print(f"\n--- 测试Header格式 {i+1} ---")
        print(f"Headers: {headers}")
        
        try:
            # 对于选项3，将token添加到URL中
            url = f"{base_url}/basic_data_service"
            if i == 2:  # 如果是选项3，尝试URL参数
                url += f"?access_token={access_token}"
            
            response = requests.post(
                url=url,
                json=test_data,
                headers=headers,
                timeout=10
            )
            
            print(f"状态码: {response.status_code}")
            try:
                result = response.json()
                print(f"错误码: {result.get('errorcode', 'N/A')}")
                print(f"错误信息: {result.get('errmsg', 'N/A')}")
                print(f"响应内容: {result}")
                
                if result.get('errorcode') == 0:
                    print("✅ 连接成功！")
                    return True
            except:
                print(f"非JSON响应: {response.text[:200]}...")
                
        except Exception as e:
            print(f"请求失败: {e}")
    
    # 尝试GET请求测试
    print(f"\n--- 测试GET请求 ---")
    try:
        response = requests.get(f"{base_url}/basic_data_service?access_token={access_token}", timeout=10)
        print(f"GET状态码: {response.status_code}")
        print(f"GET响应: {response.text[:200]}...")
    except Exception as e:
        print(f"GET请求失败: {e}")
    
    print("\n--- 尝试基础连接测试 ---")
    try:
        # 测试基础URL连接
        response = requests.get(base_url, timeout=10)
        print(f"基础URL连接: {response.status_code}")
        print(f"基础URL响应: {response.text[:200]}...")
    except Exception as e:
        print(f"基础URL连接失败: {e}")
    
    return False

def decode_jwt_token():
    """解码JWT Token查看详细信息"""
    import base64
    import json
    
    refresh_token = os.getenv("IFIND_REFRESH_TOKEN")
    if not refresh_token:
        print("❌ 未设置REFRESH_TOKEN")
        return
    
    print("\n=== JWT Token解码 ===")
    
    try:
        # JWT由三部分组成，用.分隔
        parts = refresh_token.split('.')
        if len(parts) == 3:
            # 解码payload部分 (第二部分)
            payload_part = parts[1]
            # 添加padding
            payload_part += '=' * (4 - len(payload_part) % 4)
            
            decoded_bytes = base64.b64decode(payload_part)
            payload = json.loads(decoded_bytes)
            
            print("JWT Payload内容:")
            for key, value in payload.items():
                if key == 'user':
                    print(f"  {key}: {{...}}")  # 隐藏用户详细信息
                    if isinstance(value, dict):
                        access_token = value.get('accessToken')
                        if access_token:
                            print(f"    accessToken: {access_token}")
                            print(f"    验证与环境变量中的ACCESS_TOKEN匹配: {access_token == os.getenv('IFIND_ACCESS_TOKEN')}")
                        print(f"    accessToke`nExpiredTime: {value.get('accessTokenExpiredTime')}")
                else:
                    print(f"  {key}: {value}")
        else:
            print("❌ 不是标准的JWT格式")
            
    except Exception as e:
        print(f"❌ JWT解码失败: {e}")

def main():
    decode_jwt_token()
    success = test_direct_connection()
    
    if not success:
        print("\n=== 连接失败总结 ===")
        print("""
        连接失败的可能原因：
        
        1. API端点URL可能不正确
           - 尝试: https://quantapi.51ifind.com/api/v1/basic_data_service
           - 或: https://quantapi.10jqka.com.cn/api/v1/basic_data_service
           - 或其他变体
        
        2. 参数格式可能需要调整
           - 检查codes, indicators的格式要求
           - 确认日期格式要求
        
        3. 需要特定的认证方式
           - 可能需要先进行登录认证
           - 或者需要特定的header
        
        4. 账户权限问题
           - 确认账户有API访问权限
           - 确认Token未过期（虽然JWT显示2026-01-08到期）
        """)
    else:
        print("\n✅ 连接成功！可以继续开发")

if __name__ == "__main__":
    main()
