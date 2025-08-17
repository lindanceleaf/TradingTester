# TradingTester

TradingTester 是一個簡單的 **加密貨幣策略回測框架**，透過 Python 撰寫，讓使用者可以快速測試交易策略並輸出圖表與績效統計。

## 功能特色
- **策略模組化**：將不同策略獨立於 `strategies/`，方便擴充。
- **資料擷取**：透過 [ccxt](https://github.com/ccxt/ccxt) 自動抓取 OKX 歷史 K 線。
- **技術指標**：支援 SMA、EMA、RSI 等常見技術分析指標。
- **回測系統**：
  - 資金曲線（Equity Curve）
  - 買賣訊號可視化
  - 總報酬率 / 最大回撤 / 交易次數
- **結果輸出**：自動輸出圖檔至 `results/`，檔名格式為：
  ```
  <main檔案名>_<開始日期>_<結束日期>.png
  ```
  e.g. `BTC_1x_sma_20250701_20250801.png`

## 專案結構
```
TradingTester/
├── mains/             # 各種策略的執行入口
│   ├── BTC_1x_sma.py
│   ├── BTC_1x_trend.py
│   └── ... (更多策略)
│
├── backtester/        # 回測核心
│   └── core.py
│
├── strategies/        # 策略模組
│   ├── base.py
│   ├── sma.py
│   └── trend_multi.py
│
├── utils/             # 工具
│   └── data_loader.py
│
├── results/           # 回測結果 (圖片，已忽略在 git)
│
└── venv/              # Python 虛擬環境 (已忽略在 git)
```

## 使用方式

1. **建立虛擬環境並安裝套件**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows

   pip install -r requirements.txt
   ```

2. **執行回測**
   ```bash
   python mains/BTC_1x_sma.py
   ```
   或
   ```bash
   python mains/BTC_1x_trend.py
   ```

3. **查看結果**
   - 終端機會輸出回測統計資訊  
   - `results/` 資料夾會產生對應圖檔，例如：
     ```
     BTC_1x_sma_20250701_20250801.png
     ```

## 作者
- bine0619
