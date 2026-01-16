# debug_tool_binding.py
from tools.edt_data_tool_enhanced import EnhancedEDBDataTool

def test_tool_binding():
    """测试工具绑定"""
    print("=== 工具绑定测试 ===")
    
    # 创建实例
    tool_instance = EnhancedEDBDataTool()
    print(f"工具实例类型: {type(tool_instance)}")
    
    # 获取方法
    method = tool_instance.get_basis_analysis_data
    print(f"方法类型: {type(method)}")
    print(f"方法是否可调用: {callable(method)}")
    
    # 检查方法的__self__属性
    if hasattr(method, '__self__'):
        print(f"方法绑定到实例: {method.__self__ is tool_instance}")
    else:
        print("方法没有__self__属性")
    
    # 尝试直接调用
    try:
        result = method("2024-01-01", "2024-12-31")
        print(f"直接调用成功: {result[:100]}...")
    except Exception as e:
        print(f"直接调用失败: {e}")

if __name__ == "__main__":
    test_tool_binding()
