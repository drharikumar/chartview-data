#!/usr/bin/env python3
"""Make stocks.csv (SYMBOL,SERIES) from NSE's official EQUITY_L.csv — EQ and BE series only.
   python bootstrap_stocks.py                 # download from NSE
   python bootstrap_stocks.py --file EQUITY_L.csv   # use a copy you uploaded to the repo (if NSE blocks GitHub)"""
import argparse, csv, os
from new_listings import fetch_nse

ap = argparse.ArgumentParser(); ap.add_argument("--file", default=None); a = ap.parse_args()
src = a.file if a.file else ("EQUITY_L.csv" if os.path.exists("EQUITY_L.csv") else None)
rows = fetch_nse(src)
if len(rows) < 1000: raise SystemExit("only %d EQ/BE rows — bad download, stocks.csv not written" % len(rows))
seen, out = set(), []
for r in rows:
    if r["SYMBOL"] not in seen: seen.add(r["SYMBOL"]); out.append((r["SYMBOL"], r["SERIES"]))
with open("stocks.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["SYMBOL", "SERIES"]); w.writerows(sorted(out))
print("stocks.csv: %d symbols (%s)" % (len(out), src or "downloaded from NSE"))
