import json, re
from collections import defaultdict

DATA_FILE = "/sessions/loving-wizardly-fermat/mnt/.claude/projects/C--Users-AdhamMahmoud-AppData-Roaming-Claude-local-agent-mode-sessions-ca432383-8082-4459-b484-0859f8bcc845-17689280-b17d-4dbe-83e7-9e62144aab69-local-7deccb8c-1ae0-4ad2-b3e5-608182e65a58-outputs/035c3756-8555-4f96-a97f-0d13f39b7ac9/tool-results/mcp-28138290-1612-4fb1-aaf0-f9911799cd76-looker_query-1786969133515.txt"
with open(DATA_FILE) as f:
    raw = json.load(f)
rows = raw.get('data', raw) if isinstance(raw, dict) else raw

TARGET_ZONES = {"Nasr city", "Heliopolis", "Ain shams"}
rows = [r for r in rows if r.get('dim_logistics_rider.last_operating_zone_name') in TARGET_ZONES]

CONTRACT_MAP = {"Glesco": "Gelesco"}

YDAY = "2026-08-16"
W7_START, W7_END = "2026-08-10", "2026-08-16"
MTD_START, MTD_END = "2026-08-01", "2026-08-16"
MONTH_START, MONTH_END = "2026-07-01", "2026-07-31"
W7_DAYS, MTD_DAYS, LM_DAYS = 7, 16, 31

def in_range(d, s, e): return s <= d <= e

yday_data = defaultdict(lambda: {"hrs": 0.0, "riders": 0})
w7_data   = defaultdict(lambda: {"sum_hrs": 0.0, "sum_riders": 0})
mtd_data  = defaultdict(lambda: {"sum_hrs": 0.0, "sum_riders": 0})
month_data= defaultdict(lambda: {"sum_hrs": 0.0, "sum_riders": 0})
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

INDEX_FILE = "/tmp/nasr-city-ops/index.html"
with open(INDEX_FILE) as f:
    html = f.read()

m = re.search(r'const TLP_YDAY = (\{.*?\});', html, re.DOTALL)
all_keys = list(json.loads(m.group(1)).keys()) if m else []

def r2(v): return round(v, 2)
def awh(hrs, riders): return r2(hrs/riders) if riders>0 else 0

TLP_YDAY  = {k: r2(yday_data[k]["hrs"]) for k in all_keys}
TLP_W7    = {k: r2(w7_data[k]["sum_hrs"]/W7_DAYS) for k in all_keys}
TLP_MTD   = {k: r2(mtd_data[k]["sum_hrs"]/MTD_DAYS) for k in all_keys}
TLP_MONTH = {k: r2(month_data[k]["sum_hrs"]/LM_DAYS) for k in all_keys}
TLP_RIDERS_YDAY    = {k: yday_data[k]["riders"] for k in all_keys}
TLP_RIDERS_MTD_SUM = {k: int(mtd_riders_sum[k]) for k in all_keys}
TLP_AWH_YDAY  = {k: awh(yday_data[k]["hrs"],   yday_data[k]["riders"])   for k in all_keys}
TLP_AWH_W7    = {k: awh(w7_data[k]["sum_hrs"],  w7_data[k]["sum_riders"])  for k in all_keys}
TLP_AWH_MTD   = {k: awh(mtd_data[k]["sum_hrs"], mtd_data[k]["sum_riders"]) for k in all_keys}
TLP_AWH_MONTH = {k: awh(month_data[k]["sum_hrs"],month_data[k]["sum_riders"]) for k in all_keys}

print(f"Top5 YDAY hrs: {sorted(TLP_YDAY.items(),key=lambda x:-x[1])[:5]}")
print(f"Top5 RIDERS yday: {sorted(TLP_RIDERS_YDAY.items(),key=lambda x:-x[1])[:5]}")
print(f"Ebad AWH yday: {TLP_AWH_YDAY.get('Nasr city|Ebad El rahman')}")

def patch_const(html, name, value):
    val = json.dumps(value, ensure_ascii=False)
    new, n = re.subn(rf'const {name} = \{{.*?\}};', f'const {name} = {val};', html, flags=re.DOTALL)
    print(f"  {name}: {n} sub(s)")
    return new

for name, val in [
    ("TLP_YDAY", TLP_YDAY), ("TLP_W7", TLP_W7), ("TLP_MTD", TLP_MTD), ("TLP_MONTH", TLP_MONTH),
    ("TLP_RIDERS_YDAY", TLP_RIDERS_YDAY), ("TLP_RIDERS_MTD_SUM", TLP_RIDERS_MTD_SUM),
    ("TLP_AWH_YDAY", TLP_AWH_YDAY), ("TLP_AWH_W7", TLP_AWH_W7),
    ("TLP_AWH_MTD", TLP_AWH_MTD), ("TLP_AWH_MONTH", TLP_AWH_MONTH),
]:
    html = patch_const(html, name, val)

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\n✅ Patched ({len(html)} bytes)")
