import pandas as pd
import ta

class TrendMulti:
    def __init__(self):
        self.lookback = 200  # SMA200 所需

    def generate_signals(self, df: pd.DataFrame, start_date=None):
        # === 日線 SMA (大方向) ===
        df_daily = df.resample("1D").last()
        df_daily["SMA50_D"] = df_daily["close"].rolling(50).mean()
        df_daily["SMA200_D"] = df_daily["close"].rolling(200).mean()
        df = df.join(df_daily[["SMA50_D","SMA200_D"]], how="left")
        df[["SMA50_D","SMA200_D"]] = df[["SMA50_D","SMA200_D"]].ffill()

        # === 4h EMA 與 RSI ===
        df["EMA9"] = df["close"].ewm(span=9).mean()
        df["EMA21"] = df["close"].ewm(span=21).mean()
        df["EMA50"] = df["close"].ewm(span=50).mean()
        df["MA200"] = df["close"].rolling(200).mean()
        df["RSI"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

        df["position"] = 0

        # 多頭：日線 SMA50 > SMA200
        bull = df["SMA50_D"] > df["SMA200_D"]

        # 進場（多頭 + EMA9>EMA21 + RSI>40）
        df.loc[bull & (df["EMA9"] > df["EMA21"]) & (df["RSI"] > 40), "position"] = 1

        # 出場（EMA9<EMA21 或 RSI<35）
        df.loc[(df["EMA9"] < df["EMA21"]) | (df["RSI"] < 35), "position"] = -1

        # 裁剪時間
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]

        return df
