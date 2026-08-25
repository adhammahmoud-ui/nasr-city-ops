#!/usr/bin/env python3
"""
Nasr City Ops Dashboard — Dynamic Updater v2
============================================
Reads dashboard_data.json → formats all 6 HTML sections → validates JS → writes index.html

Usage:
    python3 update_dashboard.py [path/to/dashboard_data.json]

Default JSON path: dashboard_data.json (same directory as this script)
Default HTML path: /tmp/nasr-city-ops/index.html

dashboard_data.json schema
--------------------------
{
  "zone": {
    "yday" | "wtd" | "mtd": {
      "Nasr city" | "Heliopolis" | "Ain shams": {
        "riders": int, "orders": int, "sumHrs": float, "plannedHrs": float,
        "lateLogin": float, "noShow": float, "breakMin": float,
        "acceptRate": float, "delivTime": float, "rat": float,
        "toVendor": float, "onTime": float, "failRate": float
      }
    }
  },
  "dtc_yday": { "hegaz|masaken_sh|...": [pct_float, compliant_int, total_int] },
  "dtc_mtd":  { same },
  "offenders": {
    "Nasr city" | "Heliopolis" | "Ain shams": [
      {"id": int, "noShow": int, "late": int, "breaks": float, "avp": float, "shifts": int}
    ]
  },
  "hybrid": {
    "yday" | "wtd" | "mtd": {
      "10186" | "10196" | ...: {
        "riders": int, "actHrs": float, "orders": int, "dt": float,
        "rat": float, "tv": float, "tc": float, "onTime": float,
        "planHrs": float, "noShow": float, "lateLogin": float, "breakMin": float
      }
    }
  },
  "perf": {
    "yday" | "l3d" | "l7d" | "l14d" | "mtd" | "lm": {
      "620008" | ...: {
        "orders_total": int,   -- total for the period (script divides by period_days)
        "dt": float, "rat": float, "tv": float, "tc": float, "avtc": float,
        "fir": float,          -- omit for lm period
        "ot": float,           -- raw 0-1, omit for lm
        "l10": float,          -- raw 0-1
        "l5": float            -- raw 0-1
      }
    }
  },
  "perf_shift": {
    "yday" | "l3d" | "l7d" | "l14d" | "mtd" | "lm": {
      "10186" | ...: {"l10": float, "l5": float}   -- raw 0-1
    }
  }
}

VENDOR_CODES for perf: 620008 619849 760059 801850 783048 793636 619844 717765 655461
SP_IDS for hybrid/perf_shift: 10186 10196 10198 10216 10218 10219 10229 10230
DTC MARTS: hegaz masaken_sh ard_golf omarat hay8 tayaran shorouk hadeeqa matareya
"""

import json, re, sys, calendar, tempfile, os, subprocess
from datetime import date, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
HTML_PATH  = Path('/tmp/nasr-city-ops/index.html')

# ── DATE CALCULATIONS ──────────────────────────────────────────────────────
today = date.today()
yday  = today - timedelta(days=1)

week_start   = yday - timedelta(days=yday.weekday())   # Monday
week_num     = yday.isocalendar()[1]
month_start  = yday.replace(day=1)
month_key    = yday.strftime('%Y-%m')
lm_end       = month_start - timedelta(days=1)
lm_start     = lm_end.replace(day=1)
lm_key       = lm_start.strftime('%Y-%m')
lm_days      = calendar.monthrange(lm_start.year, lm_start.month)[1]
mtd_days     = yday.day

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
MONTHS_FULL = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']

def mlbl(d):  return MONTHS[d.month - 1]
def mfull(d): return MONTHS_FULL[d.month - 1]

yday_str    = yday.strftime('%Y-%m-%d')
week_key_s  = f"{yday.isocalendar()[0]}-W{week_num:02d}"
yday_lbl    = f"{mlbl(yday)} {yday.day}, {yday.year}"
yday_short  = f"{mlbl(yday)} {yday.day}"
mtd_lbl     = f"{mlbl(month_start)} 1-{yday.day}"
lm_lbl      = mlbl(lm_start)
cur_mon_lbl = mlbl(month_start)

w7s = yday - timedelta(days=6)
w7_lbl = (f"{mlbl(w7s)} {w7s.day}-{mlbl(yday)} {yday.day}"
          if w7s.month != yday.month else f"{mlbl(yday)} {w7s.day}-{yday.day}")

if week_start.month == yday.month:
    week_range = f"{mlbl(yday)} {week_start.day}-{yday.day}"
else:
    week_range = f"{mlbl(week_start)} {week_start.day}-{mlbl(yday)} {yday.day}"

PERIOD_DAYS = {'yday': 1, 'l3d': 3, 'l7d': 7, 'l14d': 14, 'mtd': mtd_days, 'lm': lm_days}

VENDOR_ORDER = ['620008','619849','760059','801850','783048','793636','619844','717765','655461']
SP_ORDER     = [10186, 10196, 10198, 10216, 10218, 10219, 10229, 10230]
DTC_MARTS    = ['hegaz','masaken_sh','ard_golf','omarat','hay8','tayaran','shorouk','hadeeqa','matareya']

print(f"Dates → yday:{yday_str}  week:{week_key_s} (Wk {week_num})  month:{month_key}  lm:{lm_key}")
print(f"        MTD days:{mtd_days}  LM days:{lm_days}")

# ── ROUNDING HELPERS ────────────────────────────────────────────────────────
def _safe(v): return float(v) if v is not None else 0.0

def r1(v): return round(_safe(v), 1)
def r2(v): return round(_safe(v), 2)
def r3(v): return round(_safe(v), 3)
def r4(v): return round(_safe(v), 4)
def ri(v): return int(round(_safe(v)))

def sf(v, dp):
    """Format float to dp decimal places, stripping trailing zeros."""
    r = round(_safe(v), dp)
    s = f"{r:.{dp}f}".rstrip('0').rstrip('.')
    return s if s else '0'

# ── LOAD INPUT DATA ─────────────────────────────────────────────────────────
json_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SCRIPT_DIR / 'dashboard_data.json'
if not json_path.exists():
    print(f"ERROR: {json_path} not found", file=sys.stderr)
    sys.exit(1)

with open(json_path) as f:
    DATA = json.load(f)

print(f"Loaded {json_path}")

# ── ENCODING SANITIZATION ────────────────────────────────────────────────────
# These byte sequences occur when UTF-8 text is misread as Latin-1 and re-encoded
# as UTF-8 (double-encoding). Fix them before decoding.
DOUBLE_ENCODED_FIXES = [
    # U+21C4 ⇄ (swap arrows used in the dashboard swap button)
    (b'\xc3\xa2\xc2\x87\xc2\x84', '⇄'.encode('utf-8')),
    # U+2500 ─ (box-drawing dash used in CSS comments)
    (b'\xc3\xa2\xc2\x94\xc2\x80', '─'.encode('utf-8')),
    # U+2014 — (em dash)
    (b'\xc3\xa2\xc2\x80\xc2\x94', '—'.encode('utf-8')),
    # U+2018 ' (left single quote)
    (b'\xc3\xa2\xc2\x80\xc2\x98', '‘'.encode('utf-8')),
    # U+2019 ' (right single quote)
    (b'\xc3\xa2\xc2\x80\xc2\x99', '’'.encode('utf-8')),
    # U+201C " (left double quote)
    (b'\xc3\xa2\xc2\x80\xc2\x9c', '“'.encode('utf-8')),
    # U+201D " (right double quote)
    (b'\xc3\xa2\xc2\x80\xc2\x9d', '”'.encode('utf-8')),
    # U+2026 … (ellipsis)
    (b'\xc3\xa2\xc2\x80\xc2\xa6', '…'.encode('utf-8')),
]

# Text patterns that indicate double-encoding survived into the string
BAD_TEXT_PATTERNS = [
    ('â', '⇄'),   # double-encoded ⇄
    ('â', '─'),   # double-encoded ─
    ('â', '—'),   # double-encoded —
    ('â', '‘'),
    ('â', '’'),
]

def read_html_safe(path):
    """Read HTML file as bytes, fix double-encoded UTF-8 sequences, decode as UTF-8."""
    with open(path, 'rb') as f:
        raw = f.read()
    # Remove null bytes (can sneak in from bad writes)
    raw = raw.replace(b'\x00', b'')
    # Fix known double-encoded byte sequences
    for bad_bytes, good_bytes in DOUBLE_ENCODED_FIXES:
        raw = raw.replace(bad_bytes, good_bytes)
    # Decode as UTF-8
    text = raw.decode('utf-8', errors='replace')
    # Fix any double-encoded sequences that survived as text
    for bad_str, good_str in BAD_TEXT_PATTERNS:
        text = text.replace(bad_str, good_str)
    return text

def write_html_safe(path, content):
    """Write HTML as explicit UTF-8 bytes (no BOM, no encoding surprises)."""
    # Final pass: ensure no null chars crept into the string
    content = content.replace('\x00', '')
    with open(path, 'wb') as f:
        f.write(content.encode('utf-8'))

def check_encoding_issues(content):
    """Return list of any encoding problems found in the content."""
    issues = []
    # Check for double-encoded sequences as text
    for bad_str, good_str in BAD_TEXT_PATTERNS:
        count = content.count(bad_str)
        if count:
            issues.append(f"Double-encoded {repr(good_str)!r} found {count}× — auto-fixed")
    # Check for null bytes
    if '\x00' in content:
        issues.append(f"Null bytes found: {content.count(chr(0))}")
    # Check for replacement char (indicates data loss during decode)
    repl_count = content.count('�')
    if repl_count:
        issues.append(f"Unicode replacement chars (U+FFFD) found: {repl_count} — possible encoding loss")
    return issues

# ── LOAD HTML ───────────────────────────────────────────────────────────────
if not HTML_PATH.exists():
    print(f"ERROR: {HTML_PATH} not found — run: git clone ... /tmp/nasr-city-ops", file=sys.stderr)
    sys.exit(1)

html = read_html_safe(HTML_PATH)
enc_issues = check_encoding_issues(html)
for issue in enc_issues:
    print(f"⚠ Encoding: {issue}")

orig_len = len(html)
errors   = []

# ── MARKER-BASED REPLACEMENT ─────────────────────────────────────────────────
def replace_between(content, start_marker, end_marker, new_body):
    """Replace everything between markers (exclusive of markers themselves)."""
    si = content.find(start_marker)
    if si < 0: raise ValueError(f"Start marker not found: {start_marker!r}")
    ei = content.find(end_marker, si + len(start_marker))
    if ei < 0: raise ValueError(f"End marker not found: {end_marker!r}")
    after_start = content.find('\n', si) + 1
    before_end  = content.rfind('\n', 0, ei) + 1
    return content[:after_start] + new_body + '\n' + content[before_end:]


# ═══════════════════════════════════════════════════════════════════════════
# SECTION A — ZONE OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
def zone_obj(d):
    utr    = _safe(d['orders']) / _safe(d['sumHrs']) if _safe(d['sumHrs']) else 0
    avgHrs = _safe(d['sumHrs']) / _safe(d['riders']) if _safe(d['riders']) else 0
    fill   = _safe(d['sumHrs']) / _safe(d['plannedHrs']) if _safe(d['plannedHrs']) else 0
    return (
        f"{{ utr:{r4(utr)}, riders:{ri(d['riders'])}, orders:{ri(d['orders'])}, "
        f"delivComp:{ri(d['orders'])}, sumHrs:{r2(d['sumHrs'])}, avgHrs:{r3(avgHrs)}, "
        f"lateLogin:{r4(d['lateLogin'])}, noShow:{r4(d['noShow'])}, breakMin:{r2(d['breakMin'])}, "
        f"fill:{r4(fill)}, acceptRate:{r4(d['acceptRate'])}, plannedHrs:{r2(d['plannedHrs'])}, "
        f"delivTime:{r2(d['delivTime'])}, rat:{r2(d['rat'])}, toVendor:{r3(d['toVendor'])}, "
        f"onTime:{r4(d['onTime'])}, failRate:{r4(d['failRate'])}"  + (f", rr:{d['rr']}" if 'rr' in d else "") + " }"
    )

try:
    zd  = DATA['zone']
    NY  = zd['yday']['Nasr city'];  HY  = zd['yday']['Heliopolis'];  AY  = zd['yday']['Ain shams']
    NW  = zd['wtd']['Nasr city'];   HW  = zd['wtd']['Heliopolis'];   AW  = zd['wtd']['Ain shams']
    NM  = zd['mtd']['Nasr city'];   HM  = zd['mtd']['Heliopolis'];   AM  = zd['mtd']['Ain shams']

    new_day = (
        f'  "{yday_str}":{{ label:"{yday_lbl}", zones:{{\n'
        f'    "Nasr city":  {zone_obj(NY)},\n'
        f'    "Heliopolis": {zone_obj(HY)},\n'
        f'    "Ain shams":  {zone_obj(AY)}\n'
        f'  }}}},\n'
    )
    new_week = (
        f'  "{week_key_s}":{{ label:"Wk {week_num}  {week_range} (current)", '
        f'short:"Wk {week_num}", zones:{{\n'
        f'    "Nasr city": {zone_obj(NW)},\n'
        f'    "Heliopolis":{zone_obj(HW)},\n'
        f'    "Ain shams": {zone_obj(AW)}\n'
        f'  }}}},\n'
    )
    new_month = (
        f'  "{month_key}":{{ label:"{cur_mon_lbl} {yday.year} (MTD {mtd_lbl})", zones:{{\n'
        f'    "Nasr city": {zone_obj(NM)},\n'
        f'    "Heliopolis":{zone_obj(HM)},\n'
        f'    "Ain shams": {zone_obj(AM)}\n'
        f'  }}}}'
    )

    start = html.find('@@ZONE_DATA_START@@')
    end   = html.find('@@ZONE_DATA_END@@')
    zs    = html[start:end]

    # 1. Remove "(current)" from all existing week entries
    zs = re.sub(r' \(current\)"', '"', zs)

    # 2. Prepend new day entry to DAY dict
    # First clean up stale WTD entries (short:"Wk XX") that leaked into DAY section
    import re as _re
    day_s = zs.find('const DAY = {')
    day_e = zs.find('\nconst WEEK', day_s)
    if day_s >= 0 and day_e >= 0:
        day_block = zs[day_s:day_e]
        day_block = _re.sub(
            r'  "\d{4}-\d{2}-\d{2}":\{[^}]*?short:"Wk \d+",.*?\}\},\n',
            '', day_block, flags=_re.DOTALL)
        zs = zs[:day_s] + day_block + zs[day_e:]
    zs = zs.replace('const DAY = {\n', 'const DAY = {\n' + new_day, 1)

    # 3. Replace existing week entry in WEEK section, or prepend to WEEK
    wk_s = zs.find('const WEEK = {')
    wk_e = zs.find('\nconst MONTH', wk_s if wk_s >= 0 else 0)
    wk_pat = f'"{week_key_s}":'
    wk_pos = zs.find(wk_pat, wk_s if wk_s >= 0 else 0)
    in_week_section = wk_pos >= 0 and (wk_e < 0 or wk_pos < wk_e)
    if in_week_section:
        i = zs.find('{', wk_pos)
        depth = 0
        for j in range(i, len(zs)):
            if zs[j] == '{': depth += 1
            elif zs[j] == '}':
                depth -= 1
                if depth == 0:
                    end_p = j + 1
                    if end_p < len(zs) and zs[end_p] == ',': end_p += 1
                    zs = zs[:wk_pos] + new_week.rstrip() + zs[end_p:]
                    break
    else:
        if 'const WEEK = {};' in zs:
            zs = zs.replace('const WEEK = {};', 'const WEEK = {\n' + new_week + '}', 1)
        else:
            zs = zs.replace('const WEEK = {\n', 'const WEEK = {\n' + new_week, 1)

    # 4. Replace or insert current month entry
    mk_pat = f'"{month_key}":'
    mk_pos = zs.find(mk_pat)
    if mk_pos >= 0:
        i = zs.find('{', mk_pos)
        depth = 0
        for j in range(i, len(zs)):
            if zs[j] == '{': depth += 1
            elif zs[j] == '}':
                depth -= 1
                if depth == 0:
                    end_p = j + 1
                    if end_p < len(zs) and zs[end_p] == ',': end_p += 1
                    zs = zs[:mk_pos] + new_month + ',\n' + zs[end_p:]
                    break
    else:
        # Insert before previous month
        ins = zs.find(f'"{lm_key}":')
        if ins >= 0:
            zs = zs[:ins] + new_month + ',\n  ' + zs[ins:]
        else:
            if 'const MONTH = {};' in zs:
                zs = zs.replace('const MONTH = {};', 'const MONTH = {\n' + new_month + '\n}', 1)
            else:
                zs = zs.replace('const MONTH = {\n', 'const MONTH = {\n' + new_month + ',\n', 1)

    html = html[:start] + zs + html[end:]
    print("✓ ZONE section updated")
except Exception as e:
    errors.append(f"ZONE: {e}")
    print(f"✗ ZONE ERROR: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION B — 3PL (skip — data not in dashboard_data.json yet)
# ═══════════════════════════════════════════════════════════════════════════
# 3PL labels in CFG_* constants are updated here
try:
    start_3pl = html.find('@@NASR_3PL_DATA_START@@')
    if start_3pl >= 0:
        # Update only the CFG label constants — replace each one by value
        def repl_cfg(content, name, new_val):
            return re.sub(
                rf"(const {name}\s*=\s*)[^\n;]+",
                lambda m: m.group(1) + new_val + ';',
                content
            )
        s3 = html.find('@@NASR_3PL_DATA_START@@')
        e3 = html.find('@@NASR_3PL_DATA_END@@')
        seg = html[s3:e3]
        seg = repl_cfg(seg, 'CFG_YDAY_LBL',        f"'{yday_short}'")
        seg = repl_cfg(seg, 'CFG_W7_LBL',          f"'{w7_lbl}'")
        seg = repl_cfg(seg, 'CFG_MTD_LBL',         f"'{mtd_lbl}'")
        seg = repl_cfg(seg, 'CFG_MTD_DAYS',        str(mtd_days))
        seg = repl_cfg(seg, 'CFG_LAST_MONTH_LBL',  f"'{lm_lbl}'")
        seg = repl_cfg(seg, 'CFG_LAST_MONTH_DAYS', str(lm_days))
        seg = repl_cfg(seg, 'CFG_CUR_MONTH_LBL',   f"'{cur_mon_lbl}'")
        html = html[:s3] + seg + html[e3:]
        print("✓ 3PL labels updated")
except Exception as e:
    errors.append(f"3PL labels: {e}")
    print(f"✗ 3PL label ERROR: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION C — OFFENDERS
# ═══════════════════════════════════════════════════════════════════════════
def fmt_rider(r):
    return (f'{{"id":{r["id"]},"noShow":{r["noShow"]},"late":{r["late"]},'
            f'"breaks":{r2(r["breaks"])},"avp":{r2(r["avp"])},"shifts":{r["shifts"]}}}')

try:
    off = DATA['offenders']
    off_parts = []
    for zone, riders in off.items():
        riders_js = '[' + ','.join(fmt_rider(r) for r in riders) + ']'
        off_parts.append(f'"{zone}":{riders_js}')
    off_content = (
        f'const OFFENDERS = {{"{month_key}":{{"label":"{cur_mon_lbl} {yday.year}","mtd":{{'
        + ','.join(off_parts)
        + '}}};\n'
    )
    html = replace_between(html, '@@OFFENDERS_DATA_START', 'OFFENDERS_DATA_END@@ */', off_content)
    print("✓ OFFENDERS section replaced")
except Exception as e:
    errors.append(f"OFFENDERS: {e}")
    print(f"✗ OFFENDERS ERROR: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION D — DT COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════
def dtc_mart_str(d, mart):
    v = d.get(mart, [0, 0, 0])
    return f'{mart}:[{r2(v[0])},{int(v[1])},{int(v[2])}]'

try:
    dtc_y   = DATA['dtc_yday']
    dtc_m   = DATA['dtc_mtd']

    # Sanity check — v1 values should be < 90% for most marts
    high_count = sum(1 for m in DTC_MARTS if dtc_y.get(m, [0])[0] > 90)
    if high_count >= len(DTC_MARTS) // 2:
        raise ValueError(
            f"DTC YDAY values look like v2 metric ({high_count} marts > 90%). "
            "Check Looker field — use orders_on_time_talabat (v1), not v2."
        )

    new_day_line = f'"{yday_str}":{{{",".join(dtc_mart_str(dtc_y, m) for m in DTC_MARTS)}}}'
    new_month_entry = (
        f'"{month_key}":{{label:"{mfull(month_start)} {yday.year}",'
        f'marts:{{{",".join(dtc_mart_str(dtc_m, m) for m in DTC_MARTS)}}}}}'
    )

    ds_start = html.find('@@DTC_DATA_START@@')
    ds_end   = html.find('@@DTC_DATA_END@@')
    ds = html[ds_start:ds_end]

    # Replace or insert yday entry in DTC_DAYS
    old_day = re.search(rf'"{re.escape(yday_str)}"\s*:\s*\{{[^}}]+\}}', ds)
    if old_day:
        ds = ds[:old_day.start()] + new_day_line + ds[old_day.end():]
        print(f"  DTC {yday_str} day replaced")
    else:
        ds = ds.replace('const DTC_DAYS = {\n', f'const DTC_DAYS = {{\n{new_day_line},\n', 1)
        print(f"  DTC {yday_str} day inserted")

    # Replace current month entry in DTC_MONTHLY
    mk_pat2 = f'"{month_key}"'
    mk_pos2 = ds.find(mk_pat2 + '{label:')
    if mk_pos2 < 0:
        mk_pos2 = ds.find(mk_pat2 + ':')
    if mk_pos2 >= 0:
        i = ds.find('{', mk_pos2)
        depth = 0
        for j in range(i, len(ds)):
            if ds[j] == '{': depth += 1
            elif ds[j] == '}':
                depth -= 1
                if depth == 0:
                    ds = ds[:mk_pos2] + new_month_entry + ds[j+1:]
                    print(f"  DTC {month_key} monthly replaced")
                    break
    else:
        # Append before closing of DTC_MONTHLY
        ins = ds.rfind('};', ds.find('const DTC_MONTHLY'))
        if ins >= 0:
            ds = ds[:ins] + f',\n  {new_month_entry}\n' + ds[ins:]
            print(f"  DTC {month_key} monthly inserted")

    html = html[:ds_start] + ds + html[ds_end:]
    print("✓ DTC section updated")
except Exception as e:
    errors.append(f"DTC: {e}")
    print(f"✗ DTC ERROR: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION E — HYBRID
# ═══════════════════════════════════════════════════════════════════════════
def fmt_hybrid_period(sp_dict):
    """Format one period of hybrid data. sp_dict keys are string SP IDs."""
    lines = []
    for sp in SP_ORDER:
        sp_s = str(sp)
        if sp_s not in sp_dict:
            continue
        d = sp_dict[sp_s]
        riders  = _safe(d['riders'])
        actHrs  = _safe(d['actHrs'])
        orders  = int(d['orders'])
        avgHrs  = actHrs / riders if riders else 0
        utr     = orders / actHrs if actHrs else 0
        breakPct = _safe(d['breakMin']) / (avgHrs * 60) if avgHrs > 0 else 0
        lines.append(
            f'{sp}:{{utr:{r3(utr)},dt:{r2(d["dt"])},onTime:{r4(d["onTime"])},'
            f'orders:{orders},riders:{ri(riders)},acceptTime:{r3(d["rat"])},'
            f'toVendor:{r3(d["tv"])},toCustomer:{r2(d["tc"])},'
            f'actHrs:{r2(actHrs)},planHrs:{r2(d["planHrs"])},avgHrs:{r2(avgHrs)},'
            f'noShow:{r4(d["noShow"])},lateLogin:{r4(d["lateLogin"])},breakPct:{r4(breakPct)}}}'
        )
    return ',\n'.join(lines)   # CRITICAL: comma between entries

try:
    hy = DATA['hybrid']
    hybrid_content = (
        'const HYBRID_MARTS=['
        '{id:10186,label:"Ard El Golf"},{id:10196,label:"El Tayaran"},'
        '{id:10198,label:"Masaken El Shorouk"},{id:10216,label:"Masaken Sheraton"},'
        '{id:10218,label:"El Hadeeka El Dawlya"},{id:10219,label:"Ain Shams"},'
        '{id:10229,label:"Omarat El Tawfiq"},{id:10230,label:"Hay 8"}];\n'
        'const HYBRID_DATA={\n'
        '  yday:{\n' + fmt_hybrid_period(hy['yday']) + '\n  },\n'
        '  wtd:{\n'  + fmt_hybrid_period(hy['wtd'])  + '\n  },\n'
        '  mtd:{\n'  + fmt_hybrid_period(hy['mtd'])  + '\n  }\n'
        '};\n'
    )
    html = replace_between(html, '@@HYBRID_DATA_START@@', '/* @@HYBRID_DATA_END@@', hybrid_content)
    print("✓ HYBRID section replaced")
except Exception as e:
    errors.append(f"HYBRID: {e}")
    print(f"✗ HYBRID ERROR: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION F — TMART PERFORMANCE (PERF_DEL + PERF_SHIFT + PERF_DAYS)
# ═══════════════════════════════════════════════════════════════════════════
def fmt_perf_period(period, vc_dict):
    """Format one period of PERF_DEL. vc_dict keys are string vendor codes."""
    days = PERIOD_DAYS[period]
    parts = []
    for vc in VENDOR_ORDER:
        if vc not in vc_dict:
            continue
        d = vc_dict[vc]
        orders = int(round(_safe(d['orders_total']) / days))
        ot_raw = _safe(d.get('ot'))
        l10_raw = _safe(d.get('l10'))
        l5_raw  = _safe(d.get('l5'))
        entry = (
            f'"{vc}":{{'
            f'orders:{orders},'
            f'dt:{r1(d.get("dt"))},'
            f'rat:{r1(d.get("rat"))},'
            f'tv:{r1(d.get("tv"))},'
            f'tc:{r1(d.get("tc"))},'
            f'avtc:{r1(d.get("avtc"))},'
        )
        if period != 'lm':
            entry += f'fir:{r1(d.get("fir"))},ot:{r1(ot_raw * 100)},'
        entry += f'l10:{ri(l10_raw * 100)},l5:{ri(l5_raw * 100)}}}'
        parts.append(entry)
    return '{' + ','.join(parts) + '}'

def fmt_shift_period(sp_dict):
    """Format one period of PERF_SHIFT. sp_dict keys are string SP IDs.
    CRITICAL: numeric SP keys must have a colon after them: 10186:{...}
    """
    parts = []
    for sp in SP_ORDER:
        sp_s = str(sp)
        if sp_s not in sp_dict:
            continue
        d = sp_dict[sp_s]
        # sp is an integer literal key — no quotes, but colon IS required
        parts.append(f'{sp}:{{l10:{sf(d["l10"], 4)},l5:{sf(d["l5"], 4)}}}')
    return '{' + ','.join(parts) + '}'

try:
    pd   = DATA['perf']
    psd  = DATA['perf_shift']
    perf_periods = ['yday','l3d','l7d','l14d','mtd','lm']

    perf_lines = ['var PERF_DEL={']
    for i, period in enumerate(perf_periods):
        comma = ',' if i < len(perf_periods) - 1 else ''
        perf_lines.append(f'  {period}:{fmt_perf_period(period, pd[period])}{comma}')
    perf_lines.append('};')

    perf_lines.append('var PERF_SHIFT={')
    for i, period in enumerate(perf_periods):
        comma = ',' if i < len(perf_periods) - 1 else ''
        perf_lines.append(f'  {period}:{fmt_shift_period(psd[period])}{comma}')
    perf_lines.append('};')

    perf_lines.append(
        f'var PERF_DAYS={{yday:1,l3d:3,l7d:7,l14d:14,mtd:{mtd_days},lm:{lm_days}}};'
    )

    perf_content = '\n'.join(perf_lines) + '\n'
    html = replace_between(html, '@@PERF_DATA_START@@', '/* @@PERF_DATA_END@@', perf_content)
    print("✓ PERF section replaced")
except Exception as e:
    errors.append(f"PERF: {e}")
    print(f"✗ PERF ERROR: {e}")


# ── TEXT PATCHES ─────────────────────────────────────────────────────────────
try:
    # "Data as of ..." label
    html = re.sub(r'Data as of [A-Za-z]+ \d+, \d{4}', f'Data as of {yday_lbl}', html)
    # "Last 7 Days (... label)
    html = re.sub(r'Last 7 Days \([^)]+\)', f'Last 7 Days ({w7_lbl})', html)
    # MTD label
    html = re.sub(r'MTD \([^)]+\)', f'MTD ({mtd_lbl})', html)
    # Tmart Hybrid tab sync label
    html = re.sub(r'Data: Yesterday \([A-Za-z]+ \d+\)  WTD \([^)]+\)  MTD \([^)]+\)',
                  f'Data: Yesterday ({yday_short})  WTD ({week_range})  MTD ({mtd_lbl})', html)
    # Tmart Hybrid yday column header
    html = re.sub(r'(id="tpl-hdr-yday"[^>]*>)[A-Za-z]+ \d+',
                  rf'\g<1>{yday_short}', html)
    print("✓ Text patches applied")
except Exception as e:
    errors.append(f"Text patches: {e}")
    print(f"✗ Text patch ERROR: {e}")


# ── JS VALIDATION ─────────────────────────────────────────────────────────────
def validate_js(content):
    """Validate all <script> blocks with node --check. Returns list of error strings."""
    script_blocks = re.findall(r'<script[^>]*>([\s\S]*?)</script>', content, re.IGNORECASE)
    js_errors = []
    for idx, src in enumerate(script_blocks):
        if not src.strip():
            continue
        with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False, encoding='utf-8') as f:
            f.write(src)
            fname = f.name
        try:
            result = subprocess.run(
                ['node', '--check', fname],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode != 0:
                js_errors.append(f"Script block #{idx+1}: {result.stderr.strip()}")
        except FileNotFoundError:
            js_errors.append("node not found — skipping JS validation")
            break
        except subprocess.TimeoutExpired:
            js_errors.append(f"Script block #{idx+1}: node --check timed out")
        finally:
            try: os.unlink(fname)
            except: pass
    return js_errors

print("\nValidating JS...")
js_errors = validate_js(html)
if js_errors:
    for e in js_errors:
        print(f"  ✗ {e}")
    errors.extend(js_errors)
    print("ABORT: JS validation failed — not writing file")
    sys.exit(1)
else:
    print("✓ All JS blocks valid")


# ── WRITE FILE ───────────────────────────────────────────────────────────────
# Final encoding check before writing
post_issues = check_encoding_issues(html)
if post_issues:
    print("⚠ Post-processing encoding issues (auto-fixed before write):")
    for issue in post_issues:
        print(f"   • {issue}")

write_html_safe(HTML_PATH, html)

# Verify the write: read back and confirm no encoding problems
verify_bytes = HTML_PATH.read_bytes()
if b'\x00' in verify_bytes:
    errors.append(f"CRITICAL: null bytes found in written file ({verify_bytes.count(b'x00')})")
    print("✗ CRITICAL: null bytes in written file!")
else:
    print("✓ Encoding clean — no null bytes, no garbled chars")

print(f"\n✅ index.html written ({orig_len} → {len(html)} bytes, Δ{len(html)-orig_len:+d})")

# ── SUMMARY ──────────────────────────────────────────────────────────────────
if errors:
    print(f"\n⚠  {len(errors)} error(s) encountered:")
    for e in errors:
        print(f"   • {e}")
    sys.exit(2)
else:
    print("All 6 sections updated successfully.")
