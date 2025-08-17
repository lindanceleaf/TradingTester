import pandas as pd
import matplotlib.pyplot as plt
import os

class Backtester:
    def __init__(self, initial_cash=1000, leverage=1):
        """
        initial_cash: 初始資金
        leverage: 槓桿倍數 (預設 1 = 無槓桿)
        """
        self.initial_cash = initial_cash
        self.leverage = leverage

    def run(self, df: pd.DataFrame, indicators_to_plot=None, save_name="backtest.png"):
        """
        df: 包含 close, position 欄位的 DataFrame
        indicators_to_plot: dict[str, str] -> {欄位名稱: 顏色}
        """
        cash = self.initial_cash
        position = 0
        equity_curve = []

        buy_price = None
        trades = []

        buy_dates, buy_prices = [], []
        sell_dates, sell_prices = [], []

        for time, row in df.iterrows():
            price = row['close']

            # Buy
            if row['position'] == 1 and position == 0:
                position = (cash * self.leverage) / price  # 加槓桿買入
                buy_price = price
                cash = 0
                trades.append(f"Buy {time.date()} @ {price:.2f} (x{self.leverage})")
                buy_dates.append(time)
                buy_prices.append(price)

            # Sell
            elif row['position'] == -1 and position > 0:
                cash = position * price / self.leverage  # 結算槓桿
                trades.append(
                    f"Sell {time.date()} @ {price:.2f} | "
                    f"Return: {(price - buy_price) / buy_price * 100 * self.leverage:.2f}%"
                )
                position = 0
                buy_price = None
                sell_dates.append(time)
                sell_prices.append(price)

            equity = cash + (position * price if position > 0 else 0) / self.leverage
            equity_curve.append(equity)

        # === 最後強制平倉 ===
        if position > 0:
            last_time = df.index[-1]
            last_price = df['close'].iloc[-1]
            cash = position * last_price / self.leverage
            trades.append(
                f"Final Sell {last_time.date()} @ {last_price:.2f} | "
                f"Return: {(last_price - buy_price) / buy_price * 100 * self.leverage:.2f}%"
            )
            sell_dates.append(last_time)
            sell_prices.append(last_price)
            position = 0

        df['equity'] = equity_curve

        # === 繪圖 ===
        os.makedirs("results", exist_ok=True)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        # 價格
        ax1.plot(df.index, df['close'], label="Price", color="black")

        # 畫 main 指定的指標
        if indicators_to_plot:
            for col, color in indicators_to_plot.items():
                if col in df.columns:
                    ax1.plot(df.index, df[col], label=col, color=color)

        # 買賣訊號
        ax1.scatter(buy_dates, buy_prices, marker="^", color="green", label="Buy")
        ax1.scatter(sell_dates, sell_prices, marker="v", color="red", label="Sell")
        ax1.legend()
        ax1.set_title(f"Price & Signals (x{self.leverage})")

        # 資金曲線
        ax2.plot(df.index, df['equity'], label="Equity", color="green")
        ax2.legend()
        ax2.set_title("Equity Curve")

        plt.savefig(os.path.join("results", save_name), dpi=150)
        plt.close()

        # === 統計 ===
        final_value = df['equity'].iloc[-1]
        total_return = (final_value - self.initial_cash) / self.initial_cash * 100
        rolling_max = df['equity'].cummax()
        drawdown = (df['equity'] - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100

        print("=== 回測結果統整 ===")
        print(f"初始資金: {self.initial_cash:.2f}")
        print(f"最終資金: {final_value:.2f}")
        print(f"總報酬率: {total_return:.2f}%")
        print(f"最大回撤: {max_drawdown:.2f}%")
        print(f"總交易次數: {len(buy_dates)}")

        if trades:
            print("\n=== 交易明細 ===")
            for t in trades:
                print(t)

        return df
