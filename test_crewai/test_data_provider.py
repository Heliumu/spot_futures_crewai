from data_providers import get_data_provider

if __name__ == "__main__":
    print("加载数据提供者...")
    provider = get_data_provider()
    print(f"使用: {type(provider).__name__}\n")

    # 测试期货数据
    print("=== 测试期货历史数据 ===")
    try:
        data = provider.get_history_data(
            asset_class="future",
            region="cn",
            ticker="rb",
            start_date=None,
            end_date=None
        )
        print(f"获取到 {len(data)} 条数据")
        if data:
            print("示例:", data[0])
    except Exception as e:
        print("错误:", e)

    # 测试新闻数据
    print("\n=== 测试新闻数据 ===")
    try:
        news = provider.get_news_data("铜", 3)
        print(f"获取到 {len(news)} 条新闻")
        for n in news:
            print(f"- [{n.published_at}] {n.title}")
    except Exception as e:
        print("错误:", e)
