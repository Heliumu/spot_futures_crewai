# test_system_fixed.py
from main.analysis_workflow import AnalysisWorkflowFixed

def test_system():
    """测试修复后的系统"""
    workflow = AnalysisWorkflowFixed()
    
    # 测试用例
    test_inputs = [
        "沥青 半年库存分析",
        "分析沥青最近3个月的基差情况"
    ]
    
    for user_input in test_inputs:
        print("=" * 60)
        try:
            result = workflow.execute_analysis(user_input)
            print(f"\n最终结果:\n{result}\n")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_system()
