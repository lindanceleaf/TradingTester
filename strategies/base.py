import pandas as pd

class BaseStrategy:
    def __init__(self, lookback=200):
        self.lookback = lookback

    def generate_signals(self, df: pd.DataFrame, start_date: str):
        raise NotImplementedError("Strategy 必須實作 generate_signals()")
