import codecs, json, re

CSV = '/sessions/affectionate-serene-fermat/mnt/uploads/Target Compliance (12).csv'
DASH = '/tmp/nasr-city-ops/dashboard_data.json'

# Vendor name → dashboard key mapping
VENDOR_MAP = {
    'talabat mart, ard el golf':                          'ard_golf',
    'talabat mart, heliopolis - hegaz square':            'hegaz',
    'talabat mart, matareya':                             'matareya',
    'talabat mart, nasr city - el hadeeqa el dawlia':     'hadeeqa',
    'talabat mart, nasr city - el tayaran':               'tayaran',
    'talabat mart, nasr city - hay 8':                    'hay8',
    'talabat mart, nasr city - masaken el shorouk':       'shorouk',
    'tmart, masaken sheraton - abdel hamid badwai':       'masaken_sh',
    'tmart, nasr city - omarat el tawfiq':                'omarat',
}

def parse_pct(s):
    s = s.strip()
    if not s:
        return None
    try:
        return float(s.replace('%','').replace(',',''))
    except:
        return None

def parse_num(s):
    s = s.strip()
    if not s:
        return None
    try:
        return float(s.replace(',',''))
    except:
        return None

# Read CSV
with codecs.open(CSV, encoding='utf-16') as f:
    lines = f.readlines()

# Parse header dates from row 0 (0-indexed)
header = lines[0].rstrip('\n').split('\t')
# dates start at col 4
dates = [h.strip() for h in header[4:]]  # list of 'M/D/YYYY' strings
print(f"Dates found: {len(dates)}, first={dates[0]}, last={dates[-1]}")

# Parse data rows
# Structure: {vendor_key: {metric: [val_col4, val_col5, ...]}}
data = {}
i = 1
while i < len(lines):
    row = lines[i].rstrip('\n').split('\t')
    if len(row) < 5:
        i += 1
        continue
    vendor = row[2].strip().lower()
    metric = row[3].strip()
    key = VENDOR_MAP.get(vendor)
    if key is None:
        i += 1
        continue
    if key not in data:
        data[key] = {}
    values = row[4:]
    data[key][metric] = values
    i += 1

print("Parsed vendors:", list(data.keys()))

# ---- period definitions (indices into dates[] / values[]) ----
# dates[0] = 8/30, dates[6] = 8/24, dates[29] = 8/1
YDAY_IDX  = [0]               # 8/30 only
WTD_IDX   = list(range(0, 7)) # 8/30..8/24 (7 days, Mon-Sun week)
L7D_IDX   = list(range(0, 7)) # same
MTD_IDX   = list(range(0, 30)) # 8/30..8/1 (all Aug)

def weighted_avg(key, metric, idxs):
    """Orders-weighted avg DTC for given day indices."""
    orders_row = data[key].get('# Orders', [])
    dtc_row    = data[key].get('% DT Compliance', [])
    total_ord = 0
    total_wt  = 0.0
    for i in idxs:
        if i >= len(dtc_row) or i >= len(orders_row):
            continue
        dtc = parse_pct(dtc_row[i])
        ord_ = parse_num(orders_row[i])
        if dtc is None or ord_ is None:
            continue
        total_wt  += dtc * ord_
        total_ord += ord_
    if total_ord == 0:
        return None
    return round(total_wt / total_ord, 1)

# ---- compute DTC sections ----
dtc_yday = {}
dtc_wtd  = {}
dtc_l7d  = {}
dtc_mtd  = {}

for key in ['ard_golf','hegaz','matareya','hadeeqa','tayaran','hay8','shorouk','masaken_sh','omarat']:
    if key not in data:
        print(f"WARNING: {key} not found in CSV")
        dtc_yday[key] = [0.0, 0, 0]
        dtc_wtd[key]  = [0.0, 0, 0]
        dtc_l7d[key]  = [0.0, 0, 0]
        dtc_mtd[key]  = [0.0, 0, 0]
        continue

    yd  = weighted_avg(key, '% DT Compliance', YDAY_IDX)
    wtd = weighted_avg(key, '% DT Compliance', WTD_IDX)
    l7d = weighted_avg(key, '% DT Compliance', L7D_IDX)
    mtd = weighted_avg(key, '% DT Compliance', MTD_IDX)

    # total orders per period (for reference)
    def total_orders(idxs):
        row = data[key].get('# Orders', [])
        return sum(parse_num(row[i]) or 0 for i in idxs if i < len(row))

    dtc_yday[key] = [yd or 0.0,  int(total_orders(YDAY_IDX)),  0]
    dtc_wtd[key]  = [wtd or 0.0, int(total_orders(WTD_IDX)),   0]
    dtc_l7d[key]  = [l7d or 0.0, int(total_orders(L7D_IDX)),   0]
    dtc_mtd[key]  = [mtd or 0.0, int(total_orders(MTD_IDX)),   0]

# ---- print summary ----
print("\n=== YDAY (8/30) ===")
for k, v in dtc_yday.items():
    print(f"  {k}: {v[0]}%  ({v[1]} orders)")
print("\n=== WTD (8/24-8/30) ===")
for k, v in dtc_wtd.items():
    print(f"  {k}: {v[0]}%  ({v[1]} orders)")
print("\n=== MTD (8/1-8/30) ===")
for k, v in dtc_mtd.items():
    print(f"  {k}: {v[0]}%  ({v[1]} orders)")

# ---- patch dashboard_data.json ----
with open(DASH) as f:
    dash = json.load(f)

dash['dtc_yday'] = dtc_yday
dash['dtc_wtd']  = dtc_wtd
dash['dtc_l7d']  = dtc_l7d
dash['dtc_mtd']  = dtc_mtd
# dtc_lm and dtc_jul_aug carry forward (no July data in CSV)

with open(DASH, 'w') as f:
    json.dump(dash, f, indent=2)

print("\nDone. dashboard_data.json updated.")
