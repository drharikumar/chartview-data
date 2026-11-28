#!/usr/bin/env python3
"""Upstox fills what Yahoo is missing in ohlcv/daily (Yahoo stays the main source). Skips a close >25% from the last Yahoo
close (Upstox isn't split-adjusted) and new listings. Never touches Yahoo rows. No network, no token."""
import csv, datetime as dt, glob, gzip, json, os, sys
H = ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume", "Symbol"]; D = "ohlcv/daily"
def rd(p, gz=False):
    if not os.path.exists(p): return []
    with (gzip.open(p, "rt", newline="") if gz else open(p, newline="")) as f:
        r = csv.reader(f); next(r, None); return [x for x in r if len(x) == 8]
def main(days=10, gap=25.0):
    t = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=5, minutes=30)).date()
    d0, d1 = str(t - dt.timedelta(days=days)), str(t); up, yh, dl = {}, {}, {}
    for y in {d0[:4], d1[:4]}:
        for r in rd("ohlcv/upstox/HIST_OHLCV_%s.csv.gz" % y, 1):
            if d0 <= r[0] <= d1: up.setdefault(r[0], {})[r[7]] = r
    for y in {str(int(d0[:4]) - 1), d0[:4], d1[:4]}:
        for r in rd("ohlcv/history/HIST_OHLCV_%s.csv.gz" % y, 1): yh.setdefault(r[7], {})[r[0]] = float(r[2] or 0)
    for f in glob.glob(D + "/????-??-??.csv"):
        d = os.path.basename(f)[:10]; dl[d] = rd(f)
        for r in dl[d]: yh.setdefault(r[7], {})[d] = float(r[2] or 0)
    rep = {}
    for d in sorted(up):
        ys = dl.get(d, []); have = {r[7] for r in ys} | {s for s, v in yh.items() if d in v}; add = []; g = 0
        for s, r in up[d].items():
            if s in have: continue
            ref = [c for x, c in sorted(yh.get(s, {}).items()) if x < d and c > 0]
            if not ref: continue
            if abs(float(r[2]) / ref[-1] - 1) * 100 > gap: g += 1; continue
            add.append(r)
        if add:
            with open("%s/%s.csv" % (D, d), "w", newline="") as f: w = csv.writer(f); w.writerow(H); w.writerows(sorted(ys + add, key=lambda r: r[7]))
        rep[d] = [len(ys), len(add), g]; print(d, "yahoo", len(ys), "+upstox", len(add), "split-guard", g)
    ip = D + "/index.json"; ds = sorted(os.path.basename(f)[:10] for f in glob.glob(D + "/????-??-??.csv"))
    try: old = json.load(open(ip)).get("dates")
    except Exception: old = None
    if ds != old: json.dump({"dates": ds, "updated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}, open(ip, "w"))
    os.makedirs("upstox", exist_ok=True); json.dump({"days": rep, "cols": "yahoo, added from upstox, split-guard skips"}, open("upstox/fill_report.json", "w"), indent=0)
if __name__ == "__main__": main()
