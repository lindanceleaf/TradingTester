import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data
from strategies.sma import SMAStrategy
from backtester.core import Backtester

if __name__ == "__main__":
    # === 參數設定 ===
    symbol = "BTC/USDT"
    timeframe = "1d"
    start_date = "2025-07-01"
    end_date   = "2025-08-01"
    initial_cash = 1000
    leverage = 1

    # === 載入資料 ===
    strategy = SMAStrategy()
    df = load_data(symbol, timeframe, start_date, end_date, lookback=strategy.lookback)

    # === 產生訊號 ===
    df = strategy.generate_signals(df, start_date=start_date)

    # === 檔名生成 ===
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    save_name = f"{script_name}_{start_date.replace('-','')}_{end_date.replace('-','')}.png"

    # === 回測 + 畫圖 ===
    backtester = Backtester(initial_cash=initial_cash, leverage=leverage)
    df = backtester.run(df, indicators_to_plot={
        "SMA50": "blue",
        "SMA200": "orange"
    }, save_name=save_name)
