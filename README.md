# chartview-data — price data for AlphaTrace ChartView (Android)

Varun's AlphaTrace GitHub job kit (from ChartView v2.00.05) + a bootstrap step.
Must be a **PUBLIC** repo: public repos get unlimited free Actions minutes (the hourly price job alone
would use up a private repo's 2,000 free minutes a month), and the app reads the files without a token.

## Run order (Actions tab → pick the workflow → Run workflow)
1. **0 Bootstrap stock list** → `stocks.csv` (~2,000 NSE EQ/BE stocks). If it fails with 403 (NSE blocks GitHub):
   download https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv in your browser, upload it to the repo root, run again.
2. **Fundamentals** (classification + shares/float) → `fundamentals/` (slow, up to ~4 h)
3. **Historical OHLCV (Yahoo)** → `ohlcv/history/HIST_OHLCV_<year>.csv.gz` from 2010 (slow, up to ~6 h)
4. **Daily OHLCV (Yahoo)** → `ohlcv/DAILY_OHLCV.csv` + `ohlcv/daily/` (then runs hourly by itself)
5. **New listings (IPOs)** → runs weekdays by itself; run once by hand to catch up.

Optional, later (files in `optional-workflows/`; move one into `.github/workflows/` to switch it on): Daily EOD feed (NSE bhavcopy → `eod/`), Intraday (15m), Global markets, News, US feed,
Upstox jobs (need the `UPSTOX_ANALYTICS_TOKEN` secret: Settings → Secrets and variables → Actions).

Scheduled jobs start running on their own after step 1. Yahoo data is fine for our own use; it is NOT licensed
for a commercial product — swap the source before selling the app.
