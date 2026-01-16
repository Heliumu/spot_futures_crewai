
# 属性
https://default.dataset-api.aitrados.com/api/v2/future/reference/cn:jd2602?secret_key=your-api-key

https://default.dataset-api.aitrados.com/api/v2/stock/bars/cn:600000/day/from/2025-01-12/to/2025-06-12?secret_key=your-api-key&format=json&limit=30


https://default.dataset-api.aitrados.com/api/v2/future/bars/cn:rb!a1/day/latest?secret_key=your-api-key&format=json&limit=140&debug=1

https://default.dataset-api.aitrados.com/api/v2/future/bars/cn:rb!m1/day/latest?secret_key=your-api-key&format=json&limit=140&debug=1



# 实时bar
https://default.dataset-api.aitrados.com/api/v2/stock/bars/cn:600000/day/latest?secret_key=your-api-key&format=json&limit=3
https://default.dataset-api.aitrados.com/api/v2/stock/bars/us:spy/day/latest?secret_key=your-api-key&format=json
https://default.dataset-api.aitrados.com/api/v2/future/bars/cn:rb2605/day/latest?secret_key=your-api-key&format=json
https://default.dataset-api.aitrados.com/api/v2/future/bars/cn:jd2602/day/latest?secret_key=your-api-key&format=json
https://default.dataset-api.aitrados.com/api/v2/stock/bars/us:spy/day/latest?secret_key=your-api-key&format=json
https://default.dataset-api.aitrados.com/api/v2/forex/bars/GLOBAL:USDCAD/day/latest?secret_key=your-api-key&format=json
https://default.dataset-api.aitrados.com/api/v2/crypto/bars/global:btcusd/day/latest?secret_key=your-api-key&format=json
https://default.dataset-api.aitrados.com/api/v2/crypto/bars/global:btcusd/week/latest?secret_key=your-api-key&format=json

https://default.dataset-api.aitrados.com/api/v2/future/bars/cn:Y2603F/day/latest?secret_key=your-api-key&format=json

http://127.0.0.1:1235/api/v2/future/bars/cn:Y2603F/day/latest?secret_key=your-api-key&format=json

https://default.dataset-api.aitrados.com/api/v2/stock/bars/us:spy/week/latest?secret_key=your-api-key&format=json
#历史bar
https://default.dataset-api.aitrados.com/api/v2/future/bars/cn:rb2605/day/from/2025-01-12/to/2025-06-12?secret_key=your-api-key&format=json&limit=500

https://default.dataset-api.aitrados.com/api/v2/stock/bars/us:spy/day/from/2025-01-12/to/2025-06-12?secret_key=your-api-key&format=json&limit=500


https://default.dataset-api.aitrados.com/api/v2/forex/bars/GLOBAL:USDCAD/day/from/2025-01-12/to/2025-06-12?secret_key=your-api-key&format=json&limit=500

https://default.dataset-api.aitrados.com/api/v2/crypto/bars/GLOBAL:BTCUSD/day/from/2025-01-12/to/2025-06-12?secret_key=your-api-key&format=json&limit=500

https://default.dataset-api.aitrados.com/api/v2/stock/bars/us:tsla/1m/from/2025-01-12/to/2025-06-12?secret_key=your-api-key&format=json&limit=30
https://default.dataset-api.aitrados.com/api/v2/stock/bars/us:spy/1m/from/2025-12-19T00:00:00/to/2025-12-19T23:59:59?secret_key=your-api-key&format=json&limit=30

https://default.dataset-api.aitrados.com/api/v2/crypto/bars/global:btcusd/1m/from/2025-12-19T00:00:00/to/2025-12-19T23:59:59?secret_key=your-api-key&format=json&limit=1000



# 寻找连续合约的真实的合约
https://default.dataset-api.aitrados.com/api/v2/future/continuous_contracts/real_contracts/cn:rb!m1?secret_key=your-api-key

# 寻找活跃合约的真实的合约  
https://default.dataset-api.aitrados.com/api/v2/future/active_rank_contracts/real_symbol/cn:rb!a1?secret_key=your-api-key

# 当前可交易的期货合约
https://default.dataset-api.aitrados.com/api/v2/future/contracts/tradable_symbols/cn?secret_key=your-api-key


# 期权检索
https://default.dataset-api.aitrados.com/api/v2/option/search/future:cn:rb2605/call/moneyness/in_the_money?ref_asset_price=3400&secret_key=your-api-key
https://default.dataset-api.aitrados.com/api/v2/option/search/future:cn:rb/call/moneyness/in_the_money?ref_asset_price=3400&secret_key=your-api-key

# 期权过期列表
#https://default.dataset-api.aitrados.com/api/v2/option/expiration_date_list/future:cn:rb2605?secret_key=your-api-key
# https://default.dataset-api.aitrados.com/api/v2/option/expiration_date_list/future:cn:rb?secret_key=your-api-key

#https://default.dataset-api.aitrados.com/api/v2/option/expiration_date_list/future:cn:rb2605?secret_key=your-api-key&format=json&limit=30
#https://default.dataset-api.aitrados.com/api/v2/option/expiration_date_list/stock:US:SPY?secret_key=your-api-key&format=json&limit=30
#https://default.dataset-api.aitrados.com/api/v2/option/expiration_date_list/stock:CN:RB2605?secret_key=your-api-key&format=json&limit=30


# 最近的经济日历事件列表
https://default.dataset-api.aitrados.com/api/v2/economic_calendar/latest_event_list?secret_key=your-api-key&format=json&limit=5

# 检索日期
https://default.dataset-api.aitrados.com/api/v2/economic_calendar/event?secret_key=your-api-key

# 经济日历代码
https://default.dataset-api.aitrados.com/api/v2/economic_calendar/event_codes/us?secret_key=your-api-key


# 假期代码
https://default.dataset-api.aitrados.com/api/v2/holiday/holiday_codes/us?secret_key=your-api-key

# 检索假期
https://default.dataset-api.aitrados.com/api/v2/holiday/list?secret_key=your-api-key&full_symbol=STOCK:US:TSLA&from_date=2024-01-01&to_date=2026-12-31&format=json

# 检索新闻
https://default.dataset-api.aitrados.com/api/v2/news/list?secret_key=your-api-key&full_symbol=STOCK:US:TSLA&from_date=2024-01-01&to_date=2026-12-31

# 查看最新的新闻
https://default.dataset-api.aitrados.com/api/v2/news/latest?secret_key=your-api-key&full_symbol=STOCK:US:TSLA&from_date=2024-01-01&to_date=2026-12-31
https://default.dataset-api.aitrados.com/api/v2/news/latest?secret_key=your-api-key
# 查看地址
#https://default.dataset-api.aitrados.com/api/v2/server/address_info?secret_key=your-api-key