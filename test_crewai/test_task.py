# test_btc_news.py
from tools.market_data_tool import MarketDataTool

tool = MarketDataTool()
result = tool._run(
    data_type="news",
    asset_class="crypto",
    region="global",
    ticker="btcusd"
)
print(result)
