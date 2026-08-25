"""
patch_3pl.py  —  Patch 3PL performance constants in index.html

Usage:
    python patch_3pl.py <DATA_FILE> <INDEX_FILE>

DATA_FILE : path to the Looker JSON result file (from the scheduled task's
            looker_query on Logistics_PU / agg_logistics_rider_performance).
            The Looker query MUST use end_date = yday + 1 day (exclusive)
            so that yesterday's data is included. Example filter:
                "2026-07-01 to 2026-08-25"   ← to include Aug 24
            NOT:
                "2026-07-01 to 2026-08-24"   ← WRONG, excludes Aug 24

INDEX_FILE: path to the index.html to patch (e.g. the cloned repo's index.html)

All date ranges are computed automatically from today's date:
    yday      = today - 1 day
    w7        = [yday - 6 days .. yday]  (7 days ending yday)
    mtd       = [month start .. yday]
    last_month= previous full calendar month
"""

import json, re, sys
from collections import defaultdict
from datetime import date, timedelta

# ── CLI args ──────────────────────────────────────────────────────────────────
if len(sys.argv) != 3:
    print("Usage: python patch_3pl.py <DATA_FILE> <INDEX_FILE>")
    sys.exit(1)

DATA_FILE  = sys.argv[1]
INDEX_FILE = sys.argv[2]

# ── Date ranges (all computed from today) ─────────────────────────────────────
today      = date.today()
yday       = today - timedelta(days=1)

YDAY       = yday.strftime("%Y-%m-%d")

W7_END     = YDAY
W7_START   = (yday - timedelta(days=6)).strftime("%Y-%m-%d")
W7_DAYS    = 7

MTD_START  = yday.replace(day=1).strftime("%Y-%m-%d")
MTD_END    = YDAY
MTD_DAYS   = yday.day          # number of days in MTD period

# Last full calendar month
lm_last    = yday.replace(day=1) - timedelta(days=1)   # last day of prev month
lm_first   = lm_last.replace(day=1)
MONTH_START= lm_first.strftime("%Y-%m-%d")
MONTH_END  = lm_last.strftime("%Y-%m-%d")
LM_DAYS    = lm_last.day

print(f"Date ranges:")
print(f"  YDAY      = {YDAY}")
print(f"  W7        = {W7_START} → {W7_END}  ({W7_DAYS} days)")
print(f"  MTD       = {MTD_START} → {MTD_END}  ({MTD_DAYS} days)")
print(f"  LastMonth = {MONTH_START} → {MONTH_END}  ({LM_DAYS} days)")

# ── Load Looker data ──────────────────────────────────────────────────────────
with open(DATA_FILE) as f:
    raw = json.load(f)
rows = raw.get('data', raw) if isinstance(raw, dict) else raw

TARGET_ZONES = {"Nasr city", "Heliopolis", "Ain shams"}
rows = [r for r in rows if r.get('dim_logistics_rider.last_operating_zone_name') in TARGET_ZONES]

# Sanity check: verify YDAY data is present
yday_rows = [r for r in rows if r['agg_logistics_rider_performance.created_date_date'] == YDAY]
if not yday_rows:
    all_dates = sorted(set(r['agg_logistics_rider_performance.created_date_date'] for r in rows), reverse=True)
    print(f"⚠️  WARNING: No data found for YDAY={YDAY}!")
    print(f"   Latest available dates: {all_dates[:5]}")
    print(f"   This means the Looker query end_date was too early (off-by-one).")
    print(f"   Fix: use end_date = today (i.e. yday + 1), NOT yday itself.")
    sys.exit(1)

print(f"  YDAY rows found: {len(yday_rows)} ✓")

# Name normalization
CONTRACT_MAP = {"Glesco": "Gelesco"}

def in_range(d, s, e): return s <= d <= e

yday_data      = defaultdict(lambda: {"hrs": 0.0, "riders": 0})
w7_data        = defaultdict(lambda: {"sum_hrs": 0.0, "sum_riders": 0})
mtd_data       = defaultdict(lambda: {"sum_hrs": 0.0, "sum_riders": 0})
month_data     = defaultdict(lambda: {"sum_hrs": 0.0, "sum_riders": 0})
mtd_riders_sum = defaultdict(int)

for r in rows:
    zone     = r['dim_logistics_rider.last_operating_zone_name']
    contract = r['agg_logistics_rider_performance.contract_name'].strip()
    contract = CONTRACT_MAP.get(contract, contract)
    dt       = r['agg_logistics_rider_performance.created_date_date']
    riders   = int(r['agg_logistics_rider_performance.total_active_riders'] or 0)
    hrs      = float(r['agg_logistics_rider_performance.sum_actual_working_duration'] or 0.0)
    key      = f"{zone}|{contract}"

    if dt == YDAY:
        yday_data[key]["hrs"]    += hrs
        yday_data[key]["riders"] += riders

    if in_range(dt, W7_START, W7_END):
        w7_data[key]["sum_hrs"]    += hrs
        w7_data[key]["sum_riders"] += riders

    if in_range(dt, MTD_START, MTD_END):
        mtd_data[key]["sum_hrs"]    += hrs
        mtd_data[key]["sum_riders"] += riders
        mtd_riders_sum[key]         += riders

    if in_range(dt, MONTH_START, MONTH_END):
        month_data[key]["sum_hrs"]    += hrs
        month_data[key]["sum_riders"] += riders

# ── Read index.html ───────────────────────────────────────────────────────────
with open(INDEX_FILE, encoding="utf-8") as f:
    html = f.read()

# Get keys from existing TLP_YDAY constant in the HTML
m = re.search(r'const TLP_YDAY = (\{.*?\});', html, re.DOTALL)
all_keys = list(json.loads(m.group(1)).keys()) if m else []
print(f"  Keys in TLP_YDAY: {len(all_keys)}")

# ── Compute patched values ────────────────────────────────────────────────────
def r2(v): return round(v, 2)
def awh(hrs, riders): return r2(hrs / riders) if riders > 0 else 0

TLP_YDAY           = {k: r2(yday_data[k]["hrs"])                           for k in all_keys}
TLP_W7             = {k: r2(w7_data[k]["sum_hrs"] / W7_DAYS)               for k in all_keys}
TLP_MTD            = {k: r2(mtd_data[k]["sum_hrs"] / MTD_DAYS)             for k in all_keys}
TLP_MONTH          = {k: r2(month_data[k]["sum_hrs"] / LM_DAYS)            for k in all_keys}
TLP_RIDERS_YDAY    = {k: yday_data[k]["riders"]                            for k in all_keys}
TLP_RIDERS_MTD_SUM = {k: int(mtd_riders_sum[k])                           for k in all_keys}
TLP_AWH_YDAY       = {k: awh(yday_data[k]["hrs"],    yday_data[k]["riders"])    for k in all_keys}
TLP_AWH_W7         = {k: awh(w7_data[k]["sum_hrs"],  w7_data[k]["sum_riders"])  for k in all_keys}
TLP_AWH_MTD        = {k: awh(mtd_data[k]["sum_hrs"], mtd_data[k]["sum_riders"]) for k in all_keys}
TLP_AWH_MONTH      = {k: awh(month_data[k]["sum_hrs"],month_data[k]["sum_riders"]) for k in all_keys}

# Spot-check: show Ebad El rahman Nasr city
ebad_key = "Nasr city|Ebad El rahman"
print(f"\nSpot-check {ebad_key}:")
print(f"  YDAY hrs    = {TLP_YDAY.get(ebad_key)}")
print(f"  YDAY riders = {TLP_RIDERS_YDAY.get(ebad_key)}")
print(f"  AWH yday    = {TLP_AWH_YDAY.get(ebad_key)}")

# ── Patch constants in HTML ───────────────────────────────────────────────────
def patch_const(html, name, value):
    val = json.dumps(value, ensure_ascii=False)
    new, n = re.subn(rf'const {name} = \{{.*?\}};', f'const {name} = {val};', html, flags=re.DOTALL)
    print(f"  {name}: {n} substitution(s)")
    return new

print("\nPatching constants:")
for name, val in [
    ("TLP_YDAY",           TLP_YDAY),
    ("TLP_W7",             TLP_W7),
    ("TLP_MTD",            TLP_MTD),
    ("TLP_MONTH",          TLP_MONTH),
    ("TLP_RIDERS_YDAY",    TLP_RIDERS_YDAY),
    ("TLP_RIDERS_MTD_SUM", TLP_RIDERS_MTD_SUM),
    ("TLP_AWH_YDAY",       TLP_AWH_YDAY),
    ("TLP_AWH_W7",         TLP_AWH_W7),
    ("TLP_AWH_MTD",        TLP_AWH_MTD),
    ("TLP_AWH_MONTH",      TLP_AWH_MONTH),
]:
    html = patch_const(html, name, val)

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅  Patched {INDEX_FILE} ({len(html):,} bytes)")
