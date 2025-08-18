import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data
from strategies.trend_multi import TrendMulti
from backtester.core import Backtester
import pandas as pd


if __name__ == "__main__":
    symbol = "BTC/USDT"
    timeframe = "1h"
    start_date = "2025-08-03"
    end_date   = "2025-08-17"
    initial_cash = 1000
    leverage = 1

    strategy = TrendMulti()
    df = load_data(symbol, timeframe, start_date, end_date, lookback=strategy.lookback)
    df = strategy.generate_signals(df, start_date=start_date)

    # === 檔名生成 ===
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    save_name = f"{script_name}_{start_date.replace('-','')}_{end_date.replace('-','')}.png"

    backtester = Backtester(initial_cash=initial_cash, leverage=leverage)
    df = backtester.run(df, indicators_to_plot={
        "EMA9": "cyan",
        "EMA21": "red",
        "EMA50": "green",
        "MA200": "purple",
        "SMA50_D": "blue",
        "SMA200_D": "orange"
    }, save_name=save_name)

    print("\n✅ 回測完成！結果已輸出到 results 資料夾。")
