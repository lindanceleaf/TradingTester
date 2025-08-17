import pandas as pd
from strategies.base import BaseStrategy

class SMAStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(lookback=200)

    def generate_signals(self, df: pd.DataFrame, start_date: str):
        """SMA50 / SMA200 金叉死叉策略"""
        df['SMA50'] = df['close'].rolling(50).mean()
        df['SMA200'] = df['close'].rolling(200).mean()

        df['position'] = 0
        df.loc[df['SMA50'] > df['SMA200'], 'position'] = 1
        df.loc[df['SMA50'] < df['SMA200'], 'position'] = -1

        trade_start = pd.to_datetime(start_date)
        return df[df.index >= trade_start].copy()
