# tests/test_ifind_setup.py
import os
from config.ifind_config import test_ifind_connection
import dotenv

# 加载环境变量
dotenv.load_dotenv()

def main():
    print("=== iFinD 配置测试 ===")
    
    # 检查环境变量
    access_token = os.getenv("IFIND_ACCESS_TOKEN")
    refresh_token = os.getenv("IFIND_REFRESH_TOKEN")
    
    print(f"IFIND_ACCESS_TOKEN: {'已设置' if access_token else '未设置'}")
    print(f"IFIND_REFRESH_TOKEN: {'已设置' if refresh_token else '未设置'}")
    
    if access_token:
        print(f"ACCESS_TOKEN前10位: {access_token[:10]}...")
    
    # 测试连接
    test_ifind_connection()

if __name__ == "__main__":
    main()
