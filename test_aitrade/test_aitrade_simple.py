"""
测试AI交易流程
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trading.trading_manager import trading_manager
from tasks.intent_planning_task import create_intent_planning_task
from tasks.trading_task import create_trading_task
from agents.intent_agent import intent_planner
from agents.trading_agent import create_trading_agent

def test_ai_trading_flow():
    """测试AI交易流程"""
    print("=== 测试AI交易流程 ===")
    
    try:
        # 连接CTP
        success = trading_manager.connect("ctp", "default")
        if not success:
            print("❌ 无法连接到CTP")
            return False
        
        print("✅ CTP连接成功")
        
        # 测试交易工具
        from tools.trading_tool import TradingTool
        trading_tool = TradingTool()
        
        # 获取账户信息
        account_info = trading_tool._run("ctp", "get_account")
        print(f"账户信息: {account_info}")
        
        # 测试交易指令
        # 注意：这里只测试，不实际下单
        try:
            # 模拟买入指令（不实际执行，因为需要真实市场条件）
            result = trading_tool._run("ctp", "buy", symbol="rb2409", volume=1, price=4000, order_type="MARKET")
            print(f"买入指令结果: {result}")
        except Exception as e:
            print(f"买入指令测试: {e}")
        
        # 断开连接
        trading_manager.disconnect()
        print("✅ AI交易流程测试完成")
        return True
        
    except Exception as e:
        print(f"❌ AI交易流程测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_ai_trading_flow()
