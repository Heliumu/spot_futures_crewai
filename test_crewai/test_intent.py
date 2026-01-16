import json
from crewai import Crew
from pydantic import BaseModel, Field

from tasks.intent_planning_task import create_intent_planning_task
from dotenv import load_dotenv
from agents.intent_agent import intent_planner

# 0. 在所有其他导入之前，加载环境变量
load_dotenv()



# ---------------------------
# 1. 定义严格的输出格式（用于校验）
# ---------------------------
class TaskConfig(BaseModel):
    start_date: str
    end_date: str

class IntentPlan(BaseModel):
    commodity: str
    task_configs: dict[str, TaskConfig]

# ---------------------------
# 2. CrewAI Agent/Task 调用（请替换为你的真实调用）
# ---------------------------
def run_intent_task(user_query: str):
    task = create_intent_planning_task(user_query)
    crew = Crew(
        agents=[intent_planner],
        tasks=[task],
        verbose=True
    )
    result = crew.kickoff()
    return result

# ---------------------------
# 3. 交互式测试主函数
# ---------------------------
def interactive_test():
    print("=== Intent Agent 交互测试 ===")
    print("输入 query（输入 'exit' 或 'quit' 退出）\n")

    while True:
        user_input = input("请输入你的查询: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("退出测试。")
            break

        try:
            # 调用你的 CrewAI Agent/Task
            raw_result = run_intent_task(user_input)  # 替换为你的 CrewAI 调用

            # 校验并输出
            plan = IntentPlan(**raw_result)
            print("\n✅ 输出合法，符合 IntentPlan 结构！")
            print(json.dumps(plan.model_dump(), indent=2, ensure_ascii=False))
        except Exception as e:
            print("\n❌ 输出不符合结构或执行出错：", e)
        print("\n" + "-"*50 + "\n")

# ---------------------------
# 4. 启动交互
# ---------------------------
if __name__ == "__main__":
    interactive_test()
