import ccxt
import pandas as pd
import time

def fetch_ohlcv_range(symbol: str, timeframe: str, since: int, until: int, limit=1000):
    """分批抓取 K 線直到 until"""
    exchange = ccxt.okx()
    all_data = []
    fetch_since = since

    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=fetch_since, limit=limit)
        if not ohlcv:
            break

        all_data.extend(ohlcv)

        last_ts = ohlcv[-1][0]
        if last_ts >= until:
            break

        # 避免 API 被 ban
        fetch_since = last_ts + 1
        time.sleep(0.2)

    df = pd.DataFrame(all_data, columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    df = df[df.index <= pd.to_datetime(until, unit='ms')]
    return df


def load_data(symbol: str, timeframe: str, start_date: str, end_date: str, lookback: int = 200):
    """抓取 [start_date - lookback] 到 end_date 的完整資料"""
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    since_dt = start_dt - pd.Timedelta(days=lookback)

    since_ms = int(since_dt.timestamp() * 1000)
    until_ms = int(end_dt.timestamp() * 1000)

    df = fetch_ohlcv_range(symbol, timeframe, since_ms, until_ms)
    return df
