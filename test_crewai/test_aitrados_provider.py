# test_aitrados_provider.py
from data_providers import get_data_provider
import os

def main():
    print("🚀 开始测试 AitradosDataProvider...\n")

    # 设置为 aitrados 模式
    os.environ["DATA_PROVIDER"] = "aitrados"
    
    try:
        provider = get_data_provider()
        print(f"✅ 成功加载: {type(provider).__name__}\n")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return

    # --- 测试 1: 期货历史数据 ---
    print("=== 测试 1: 获取期货历史数据 ===")
    try:
        data = provider.get_history_data(
            asset_class="future",
            region="cn",
            ticker="rb!a1",   # 主力连续合约
            start_date=None,
            end_date=None
        )
        print(f"✅ 成功获取到 {len(data)} 条期货K线数据")
        if data:
            print("示例:", data[0])
    except Exception as e:
        print(f"❌ 失败: {e}")

    # --- 测试 2: 获取新闻数据 ---
    print("\n=== 测试 2: 获取新闻数据 ===")
    try:
        # ✅ 使用 full_symbol 格式（不是 query）
        full_symbol = "CRYPTO:GLOBAL:BTCUSD"  # BTC 的标准格式
        news = provider.get_news_by_symbol(full_symbol, limit=3)
        
        print(f"✅ 成功获取到 {len(news)} 条新闻")
        for n in news:
            print(f"- [{n.published_at}] {n.title} (来源: {n.source})")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # --- 测试 3: 经济日历 ---
    print("\n=== 测试 3: 获取经济日历事件 ===")
    try:
        events = provider.get_economic_events(days_ahead=5)
        print(f"✅ 成功获取到 {len(events)} 条经济事件")
        for e in events:
            print(f"- [{e.release_time}] {e.event_name} ({e.country}, 重要性:{e.importance})")
    except Exception as e:
        print(f"❌ 失败: {e}")

if __name__ == "__main__":
    main()
