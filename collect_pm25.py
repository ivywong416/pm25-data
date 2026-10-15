#!/usr/bin/env python3
"""每小时抓取新加坡 PM2.5(data.gov.sg 官方 API),追加到 CSV(自动去重)。
cron 示例(每小时第 2 分钟):  2 * * * * /usr/bin/python3 /path/collect_pm25.py
"""
import csv, os, requests

API = "https://api-open.data.gov.sg/v2/real-time/api/pm25"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sg_pm25_history.csv")
COLS = ["timestamp", "north", "south", "east", "west", "central"]

seen = set()
if os.path.exists(OUT):
    with open(OUT, newline="") as f:
        seen = {r["timestamp"] for r in csv.DictReader(f)}

items = requests.get(API, timeout=30).json()["data"]["items"]
new = os.path.exists(OUT)
with open(OUT, "a", newline="") as f:
    w = csv.writer(f)
    if not new:
        w.writerow(COLS)
    for it in items:
        ts = it["timestamp"]
        r = it["readings"]["pm25_one_hourly"]
        if ts not in seen:
            w.writerow([ts] + [r[c] for c in COLS[1:]])
            print("saved", ts)
