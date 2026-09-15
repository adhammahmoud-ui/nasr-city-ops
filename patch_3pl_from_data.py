"""Patch TLP constants in index.html from dashboard_data.json (pre-aggregated)."""
import json, re, sys

DATA_FILE  = 'dashboard_data.json'
INDEX_FILE = 'index.html'

with open(DATA_FILE) as f:
    d = json.load(f)

TLP_VARS = [
    ('TLP_YDAY',           d['tlp_yday']),
    ('TLP_W7',             d['tlp_w7']),
    ('TLP_MTD',            d['tlp_mtd']),
    ('TLP_MONTH',          d['tlp_month']),
    ('TLP_RIDERS_YDAY',    d['tlp_riders_yday']),
    ('TLP_RIDERS_MTD_SUM', d['tlp_riders_mtd_sum']),
    ('TLP_AWH_YDAY',       d['tlp_awh_yday']),
    ('TLP_AWH_W7',         d['tlp_awh_w7']),
    ('TLP_AWH_MTD',        d['tlp_awh_mtd']),
    ('TLP_AWH_MONTH',      d['tlp_awh_month']),
]

with open(INDEX_FILE) as f:
    html = f.read()

count = 0
for varname, data in TLP_VARS:
    new_val = json.dumps(data, separators=(',',':'))
    pattern = rf'const {varname}\s*=\s*\{{[^;]*?\}};'
    replacement = f'const {varname} = {new_val};'
    new_html, n = re.subn(pattern, replacement, html, flags=re.DOTALL)
    if n == 0:
        print(f"  ⚠️  {varname}: pattern not found")
    else:
        html = new_html
        count += 1
        print(f"  ✓ {varname}: {len(data)} keys")

with open(INDEX_FILE, 'w') as f:
    f.write(html)

print(f"\n✓ 3PL patch done: {count}/{len(TLP_VARS)} vars updated")
