# -*- coding: utf-8 -*-
# -------------------------------------------------------
# 文件类型: 技术指标
# 帮助文档: https://qmfquant.com/static/doc/code/indicatorEdit.html
# 期魔方，为您提供专业的量化服务
# -------------------------------------------------------

"""描述：指标外置参数说明
    用于定义指标的可配置参数，如周期、数值等
重要：
    请使用is_main参数区分主图指标和副图指标
    主图指标的is_main为True，副图指标的is_main为False
"""

from pydantic import BaseModel, Field


class Params(BaseModel, validate_assignment=True):
    """指标参数配置类"""
    is_main: bool = Field(default=True, title="是否为主图")
    len_thma: int = Field(default=40, title='移动平均线计算周期')
    len_vol: int = Field(default=15, title='波动率计算周期')
    length_atr: int = Field(default=20, title='ATR计算周期')


# ============================================================
# 可选方法区
# ============================================================

def on_auth(self):
    """描述：验证用户是否有权限运行该指标文件"""
    pass


def on_subscribe(self):
    """描述：订阅其他品种或周期的数据"""
    pass


# ============================================================
# 必选方法区
# ============================================================

def on_init(self):
    """描述：初始化方法，自定义属性及图形等"""
    import numpy as np
    import pandas as pd

    # 日志记录器
    self.logger = self.Logger('C:\\Users\\Admin\\Desktop\\test_msg.log')
    self.logger.info('初始化成功')

    # 数据存储
    self.df = pd.DataFrame()
    self.datetime_str = None

    # 文本对象
    self.text_line = self.MultiText('multi_text')
    self.line_up = self.Text('text_line')
    self.line_low = self.Text('text_line')

    # 颜色定义
    self.color_up = 'rgba(22, 229, 160, 1)'    # 绿色 #16e5a0
    self.color_down = 'rgba(116, 29, 221, 1)'  # 紫色 #741ddd

    # 蜡烛图对象（上涨和下跌使用不同颜色）
    self.bar_up = self.Bar('bar_up', self.color_up, width=32, type=0)   # 上涨实体
    self.bar_dn = self.Bar('bar_dn', self.color_down, width=32, type=0) # 下跌实体

    # 图形元素容器
    self.candles = []           # 蜡烛图列表
    self.triangles_up = []      # 向上三角形信号列表
    self.triangles_dn = []      # 向下三角形信号列表

    # 趋势状态
    self.trend = ""


def calculate_all(self, data):
    """描述：计算指标输出对象的值（全量计算）"""
    import talib as ta
    import numpy as np
    import pandas as pd

    # 解包数据
    length, datetime_str, open_p, high, low, close, volume = data
    self.datetime_str = datetime_str

    # 构建DataFrame
    list_data = [datetime_str, open_p, high, low, close, volume]
    list_name = ['datetime_str', 'open', 'high', 'low', 'close', 'volume']
    for i in range(len(list_data)):
        self.df[list_name[i]] = list_data[i]
    df = self.df

    # ------------------
    # 指标计算函数
    # ------------------
    def HMA(s, period):
        """Hull移动平均线"""
        return ta.WMA(
            ta.WMA(s, period // 2).multiply(2).sub(ta.WMA(s, period)),
            int(np.sqrt(period))
        )

    def THMA(s, period):
        """三重移动平均线"""
        return ta.WMA(
            ta.WMA(s, int(period / 3)) * 3 - 
            ta.WMA(s, int(period / 2)) - 
            ta.WMA(s, period),
            period
        )

    # ------------------
    # 计算指标值
    # ------------------
    df['volatility'] = HMA(df['high'] - df['low'], self.params.len_vol)
    df['thma'] = THMA(df['close'], self.params.len_thma)
    df['thma_1'] = df['thma'].shift(1)
    df['thma_2'] = df['thma'].shift(2)
    df['atr'] = ta.ATR(df['high'], df['low'], df['close'], self.params.length_atr)

    # 信号计算
    df['signal'] = df['thma'] > df['thma_2']
    df['signal_yes'] = df['signal'].shift(1)
    df['signal_up'] = (df['signal'] == True) & (df['signal_yes'] == False)   # 金叉
    df['signal_dn'] = (df['signal'] == False) & (df['signal_yes'] == True)  # 死叉

    # 上下边界
    df['up'] = df['thma'] + df['volatility']
    df['low'] = df['thma'] - df['volatility']

    # ------------------
    # 绘制蜡烛图和信号
    # ------------------
    for i in df.index[2:]:  # 从索引2开始，因为需要thma_2
        if pd.isna(df['thma'][i]) or pd.isna(df['thma_2'][i]) or pd.isna(df['volatility'][i]):
            continue

        # 蜡烛图数据
        candle_open = df['thma'][i]
        candle_high = df['thma'][i] + df['volatility'][i]
        candle_low = df['thma_2'][i] - df['volatility'][i]
        candle_close = df['thma_2'][i]

        # 确定颜色和方向
        is_up = df['signal'][i]
        color_u = self.color_up if is_up else self.color_down
        color_d = self.color_down

        # 透明度设置
        fill_alpha = 40 / 100
        border_alpha = 40 / 100

        fill_color = f'rgba(22, 229, 160, {fill_alpha})' if is_up else f'rgba(116, 29, 221, {fill_alpha})'
        border_color = f'rgba(22, 229, 160, {border_alpha})' if is_up else f'rgba(116, 29, 221, {border_alpha})'

        time_center = df['datetime_str'][i]

        # 绘制蜡烛实体
        if i > 0:
            entity_high = max(candle_open, candle_close)
            entity_low = min(candle_open, candle_close)

            if is_up:
                self.bar_up.set_point(time_center, entity_low, entity_high)
            else:
                self.bar_dn.set_point(time_center, entity_low, entity_high)

            # 上影线
            if candle_high > entity_high:
                shadow_up = self.Polygon(f'shadow_up_{i}', border_color, bg_color=fill_color, line_width=1)
                mid_time = time_center
                shadow_up.set_segment(self.CornerSegment(f'shadow_up_{i}_1', mid_time, entity_high))
                shadow_up.set_segment(self.CornerSegment(f'shadow_up_{i}_2', mid_time, candle_high))
                self.candles.append(shadow_up)

            # 下影线
            if candle_low < entity_low:
                shadow_dn = self.Polygon(f'shadow_dn_{i}', border_color, bg_color=fill_color, line_width=1)
                mid_time = time_center
                shadow_dn.set_segment(self.CornerSegment(f'shadow_dn_{i}_1', mid_time, entity_low))
                shadow_dn.set_segment(self.CornerSegment(f'shadow_dn_{i}_2', mid_time, candle_low))
                self.candles.append(shadow_dn)

        # 绘制三角形信号
        if not pd.isna(df['atr'][i]) and not pd.isna(df['thma_2'][i]):
            # 向上信号
            if df['signal_up'][i]:
                tri_up_small = self.Text(f'tri_up_small_{i}')
                tri_up_small.set_point(time_center, df['thma_2'][i] - df['atr'][i], '▲',
                                      color=color_u, font='16px')
                self.triangles_up.append(tri_up_small)

                tri_up_large = self.Text(f'tri_up_large_{i}')
                tri_up_large.set_point(time_center, df['thma_2'][i] - df['atr'][i], '▲',
                                       color='rgba(22, 229, 160, 0.6)', font='20px')
                self.triangles_up.append(tri_up_large)

            # 向下信号
            if df['signal_dn'][i]:
                tri_dn_small = self.Text(f'tri_dn_small_{i}')
                tri_dn_small.set_point(time_center, df['thma_2'][i] + df['atr'][i], '▼',
                                       color=color_d, font='16px')
                self.triangles_dn.append(tri_dn_small)

                tri_dn_large = self.Text(f'tri_dn_large_{i}')
                tri_dn_large.set_point(time_center, df['thma_2'][i] + df['atr'][i], '▼',
                                       color='rgba(116, 29, 221, 0.6)', font='20px')
                self.triangles_dn.append(tri_dn_large)


def calculate_last(self, data):
    """描述：计算指标输出对象的值（增量计算）"""
    import talib as ta
    import numpy as np
    import pandas as pd

    df = self.df
    datetime_str, open_p, high, low, close, volume = data

    # 新数据时才计算
    if datetime_str != self.datetime_str[-1]:
        self.datetime_str.append(datetime_str)

        # 追加新数据到DataFrame
        df_new = pd.DataFrame({
            'datetime_str': [datetime_str],
            'open': [open_p],
            'high': [high],
            'low': [low],
            'close': [close],
            'volume': [volume]
        })
        df = df._append(df_new, ignore_index=True)
        self.df = df

        # 指标计算函数
        def HMA(s, period):
            """Hull移动平均线"""
            return ta.WMA(
                ta.WMA(s, period // 2).multiply(2).sub(ta.WMA(s, period)),
                int(np.sqrt(period))
            )

        def THMA(s, period):
            """三重移动平均线"""
            return ta.WMA(
                ta.WMA(s, int(period / 3)) * 3 - 
                ta.WMA(s, int(period / 2)) - 
                ta.WMA(s, period),
                period
            )

        # 计算指标
        df['volatility'] = HMA(df['high'] - df['low'], self.params.len_vol)
        df['thma'] = THMA(df['close'], self.params.len_thma)
        df['thma_2'] = df['thma'].shift(2)
        df['atr'] = ta.ATR(df['high'], df['low'], df['close'], self.params.length_atr)
        df['signal'] = df['thma'] > df['thma_2']
        df['signal_yes'] = df['signal'].shift(1)
        df['signal_up'] = (df['signal'] == True) & (df['signal_yes'] == False)   # 金叉
        df['signal_dn'] = (df['signal'] == False) & (df['signal_yes'] == True)  # 死叉
        df['up'] = df['thma'] + df['volatility']
        df['low'] = df['thma'] - df['volatility']

        # 获取最后一根数据的索引
        i = df.index[-1]

        # 颜色定义
        color_u = self.color_up
        color_d = self.color_down

        # 绘制最后一根蜡烛图
        if (i >= 2 and 
            not pd.isna(df['thma'][i]) and 
            not pd.isna(df['thma_2'][i]) and 
            not pd.isna(df['volatility'][i])):

            candle_open = df['thma'][i]
            candle_high = df['thma'][i] + df['volatility'][i]
            candle_low = df['thma_2'][i] - df['volatility'][i]
            candle_close = df['thma_2'][i]

            is_up = df['signal'][i]
            fill_alpha = 40 / 100
            border_alpha = 40 / 100

            fill_color = f'rgba(22, 229, 160, {fill_alpha})' if is_up else f'rgba(116, 29, 221, {fill_alpha})'
            border_color = f'rgba(22, 229, 160, {border_alpha})' if is_up else f'rgba(116, 29, 221, {border_alpha})'

            time_center = df['datetime_str'][i]

            # 蜡烛实体
            entity_high = max(candle_open, candle_close)
            entity_low = min(candle_open, candle_close)

            if is_up:
                self.bar_up.set_point(time_center, entity_low, entity_high)
            else:
                self.bar_dn.set_point(time_center, entity_low, entity_high)

            # 上影线
            if candle_high > entity_high:
                shadow_up = self.Polygon(f'shadow_up_{i}', border_color, bg_color=fill_color, line_width=1)
                mid_time = time_center
                shadow_up.set_segment(self.CornerSegment(f'shadow_up_{i}_1', mid_time, entity_high))
                shadow_up.set_segment(self.CornerSegment(f'shadow_up_{i}_2', mid_time, candle_high))
                self.candles.append(shadow_up)

            # 下影线
            if candle_low < entity_low:
                shadow_dn = self.Polygon(f'shadow_dn_{i}', border_color, bg_color=fill_color, line_width=1)
                mid_time = time_center
                shadow_dn.set_segment(self.CornerSegment(f'shadow_dn_{i}_1', mid_time, entity_low))
                shadow_dn.set_segment(self.CornerSegment(f'shadow_dn_{i}_2', mid_time, candle_low))
                self.candles.append(shadow_dn)

        # 绘制三角形信号
        if not pd.isna(df['atr'][i]) and not pd.isna(df['thma_2'][i]):
            time_curr = df['datetime_str'][i]

            # 向上信号
            if df['signal_up'][i]:
                tri_up_small = self.Text(f'tri_up_small_{i}')
                tri_up_small.set_point(time_curr, df['thma_2'][i] - df['atr'][i], '▲',
                                       color=color_u, font='16px')
                self.triangles_up.append(tri_up_small)

                tri_up_large = self.Text(f'tri_up_large_{i}')
                tri_up_large.set_point(time_curr, df['thma_2'][i] - df['atr'][i], '▲',
                                       color='rgba(22, 229, 160, 0.6)', font='20px')
                self.triangles_up.append(tri_up_large)

            # 向下信号
            if df['signal_dn'][i]:
                tri_dn_small = self.Text(f'tri_dn_small_{i}')
                tri_dn_small.set_point(time_curr, df['thma_2'][i] + df['atr'][i], '▼',
                                       color=color_d, font='16px')
                self.triangles_dn.append(tri_dn_small)

                tri_dn_large = self.Text(f'tri_dn_large_{i}')
                tri_dn_large.set_point(time_curr, df['thma_2'][i] + df['atr'][i], '▼',
                                       color='rgba(116, 29, 221, 0.6)', font='20px')
                self.triangles_dn.append(tri_dn_large)
