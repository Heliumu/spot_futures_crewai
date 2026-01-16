# config/check_setup.py
import os
from dotenv import load_dotenv

def check_environment():
    """检查环境配置"""
    load_dotenv()
    
    required_vars = ['IFIND_ACCESS_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        print("请在 .env 文件中设置:")
        print("IFIND_ACCESS_TOKEN=your_token_here")
        return False
    
    print("✅ 环境配置检查通过")
    return True

if __name__ == "__main__":
    check_environment()
