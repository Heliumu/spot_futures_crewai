# config/ifind_auth.py
"""
关于iFinD的认证信息：

1. **ACCESS_TOKEN**: 
   - 通常是通过登录获取的临时令牌
   - 有有效期限制，需要定期刷新
   - 用于API请求的身份验证

2. **REFRESH_TOKEN**:
   - 用于刷新ACCESS_TOKEN的长期令牌
   - 通常有效期更长
   - 用于获取新的ACCESS_TOKEN

获取方法：
1. 登录iFinD官网或客户端
2. 在账户设置或API管理页面找到API密钥
3. 通常会提供ACCESS_TOKEN和REFRESH_TOKEN
4. 如果您看到的refreshToken下的request值就是ACCESS_TOKEN，可以尝试使用

建议的配置方式：
"""
import os
from typing import Optional

def get_ifind_credentials() -> tuple[str, str]:
    """
    获取iFinD认证信息
    返回 (access_token, refresh_token)
    """
    access_token = os.getenv("IFIND_ACCESS_TOKEN")
    refresh_token = os.getenv("IFIND_REFRESH_TOKEN")
    
    if not access_token:
        # 尝试使用refreshToken作为access_token（如果这是您的情况）
        refresh_token = os.getenv("IFIND_REFRESH_TOKEN")
        if refresh_token:
            access_token = refresh_token
            print("⚠️ 使用IFIND_REFRESH_TOKEN作为ACCESS_TOKEN，请确认这是否正确")
    
    if not access_token:
        raise ValueError("""
        请设置IFIND_ACCESS_TOKEN环境变量。
        您可以通过以下方式获取：
        1. 登录同花顺iFinD账户
        2. 进入API管理页面
        3. 申请或查看API密钥
        4. 将获取的token设置到环境变量中
        """)
    
    return access_token, refresh_token

# 测试连接
def test_ifind_connection():
    """测试iFinD连接"""
    try:
        access_token, refresh_token = get_ifind_credentials()
        print(f"✅ 已获取ACCESS_TOKEN: {access_token[:10]}...")
        
        # 创建客户端测试连接
        from data_providers.ifind_http_client import IFinDHTTPClient
        client = IFinDHTTPClient()
        print("✅ iFinD HTTP客户端初始化成功")
        
        # 可以尝试获取一个简单的数据点来测试
        # result = client.get_real_time_quotation(["300033.SZ"])
        # print("✅ 连接测试成功")
        
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        print("请检查您的iFinD认证信息是否正确设置")
