# search_ctp_error_in_lib.py
import os
import sys
import subprocess
from pathlib import Path

def search_ctp_error_in_system():
    """在系统库中搜索CTP错误字符串"""
    print("🔍 在系统库中搜索CTP错误字符串...")
    
    # 获取Python安装路径
    python_paths = [
        sys.prefix,
        sys.base_prefix,
        getattr(sys, '_base_executable', ''),
    ]
    
    # 常见的包安装路径
    common_paths = [
        Path(sys.prefix) / "lib" / "python3.12" / "site-packages",
        # Path(sys.prefix) / "lib" / "python3.10" / "site-packages", 
        # Path(sys.prefix) / "lib" / "python3.9" / "site-packages",
        Path.home() / ".local" / "lib" / "python3.12" / "site-packages",
        # Path.home() / ".local" / "lib" / "python3.10" / "site-packages",
        # Path.home() / ".local" / "lib" / "python3.9" / "site-packages",
    ]
    
    # 添加虚拟环境路径
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        venv_site_packages = Path(sys.prefix) / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
        common_paths.insert(0, venv_site_packages)
    
    search_terms = [
        "不合法的登录",
        # "not a valid login",
        # "invalid login",
        # "code 3",
        # "错误代码3",
        # "login failed"
    ]
    
    found_files = []
    
    for search_path in common_paths:
        if search_path.exists():
            print(f"\n🔍 搜索路径: {search_path}")
            for py_file in search_path.rglob("*.py"):
                try:
                    with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for term in search_terms:
                            if term in content:
                                found_files.append((py_file, term))
                                print(f"   ✅ 找到 '{term}' 在: {py_file}")
                except:
                    continue
    
    return found_files

def search_ctp_binaries():
    """搜索CTP相关的二进制文件和动态库"""
    print("\n🔍 搜索CTP相关的二进制文件...")
    
    # 搜索可能包含CTP API的二进制文件
    search_paths = [
        Path(sys.prefix),
        Path.home() / ".local",
        Path("/usr/local"),
        Path("/opt"),
    ]
    
    binary_extensions = [".so", ".dll", ".dylib", ".pyd"]
    
    for search_path in search_paths:
        if search_path.exists():
            print(f"🔍 搜索二进制文件在: {search_path}")
            for ext in binary_extensions:
                for bin_file in search_path.rglob(f"*{ext}"):
                    if 'ctp' in bin_file.name.lower():
                        print(f"   📁 找到CTP二进制文件: {bin_file}")

def search_with_grep():
    """使用系统grep命令搜索（如果可用）"""
    print("\n🔍 尝试使用系统命令搜索...")
    
    try:
        # 查找Python包路径
        result = subprocess.run([
            sys.executable, "-c", 
            "import site; print('\\n'.join(site.getsitepackages()))"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            site_packages = result.stdout.strip().split('\n')
            for package_path in site_packages:
                if os.path.exists(package_path):
                    print(f"📁 在 {package_path} 中搜索...")
                    
                    # 使用grep搜索错误字符串
                    try:
                        grep_result = subprocess.run([
                            'grep', '-r', '-n', '不合法的登录', package_path
                        ], capture_output=True, text=True, timeout=10)
                        
                        if grep_result.stdout:
                            print(f"   ✅ 找到匹配内容:")
                            for line in grep_result.stdout.split('\n')[:10]:  # 只显示前10行
                                if line.strip():
                                    print(f"      {line}")
                        else:
                            print(f"   ❌ 未找到匹配内容")
                            
                    except subprocess.TimeoutExpired:
                        print(f"   ⏰ 搜索超时")
                    except Exception as e:
                        print(f"   ❌ grep命令失败: {e}")
    except Exception as e:
        print(f"❌ 无法执行系统命令: {e}")

def inspect_aitrados_broker_structure():
    """检查aitrados_broker的目录结构"""
    print("\n🔍 检查aitrados_broker目录结构...")
    
    try:
        import aitrados_broker
        broker_path = Path(aitrados_broker.__file__).parent
        print(f"📁 aitrados_broker 路径: {broker_path}")
        
        def print_directory_tree(path, prefix="", max_depth=3, current_depth=0):
            if current_depth >= max_depth:
                return
                
            items = list(path.iterdir())
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                
                if item.is_dir():
                    print(f"{prefix}{current_prefix}{item.name}/")
                    print_directory_tree(item, prefix + ("    " if is_last else "│   "), max_depth, current_depth + 1)
                else:
                    print(f"{prefix}{current_prefix}{item.name}")
        
        print_directory_tree(broker_path)
        
    except ImportError:
        print("❌ 无法导入aitrados_broker")
    except Exception as e:
        print(f"❌ 检查失败: {e}")

def find_ctp_gateway_mapping():
    """寻找CTP网关配置映射代码"""
    print("\n🔍 寻找CTP网关配置映射代码...")
    
    try:
        import aitrados_broker
        broker_path = Path(aitrados_broker.__file__).parent
        
        # 搜索包含映射逻辑的文件
        mapping_keywords = [
            'ctp', 'gateway', 'map', 'config', 'setting', 'translate', 
            'convert', 'transform', 'mapping', 'connect', 'login'
        ]
        
        for py_file in broker_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    # 检查是否包含CTP相关的关键词
                    if any(keyword in content for keyword in mapping_keywords):
                        print(f"🔍 检查文件: {py_file}")
                        
                        # 查找配置处理相关的代码段
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if 'userid' in line or 'password' in line or 'broker' in line:
                                print(f"   行 {i+1}: {line.strip()}")
                                
            except:
                continue
                
    except Exception as e:
        print(f"❌ 搜索失败: {e}")

def main():
    print("🔧 CTP错误源深度搜索工具")
    
    # 1. 搜索错误字符串
    found_files = search_ctp_error_in_system()
    
    # 2. 搜索二进制文件
    search_ctp_binaries()
    
    # 3. 使用系统命令搜索
    search_with_grep()
    
    # 4. 检查目录结构
    inspect_aitrados_broker_structure()
    
    # 5. 寻找映射代码
    find_ctp_gateway_mapping()
    
    print(f"\n📊 搜索完成，找到 {len(found_files)} 个包含错误字符串的文件")

if __name__ == "__main__":
    main()
