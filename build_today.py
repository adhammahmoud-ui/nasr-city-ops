import json, re
from datetime import date, timedelta
import calendar

today = date(2026, 9, 15)
yday  = date(2026, 9, 14)
week_start = date(2026, 9, 14)
month_start = date(2026, 9, 1)
lm_start = date(2026, 8, 1)
lm_end   = date(2026, 8, 31)
MTD_DAYS = 14
LM_DAYS  = 31
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def r2(v): return round(float(v), 2)
def r4(v): return round(float(v), 4)

# ── TABLEAU zone data ─────────────────────────────────────────────────────────
tableau_yday = {
    "Nasr city":  {"sumHrs":14082.03,"orders":28597,"delivTime":22.08,"rat":6.84,"toVendor":3.28,"onTime":0.85,"failRate":0.0246},
    "Heliopolis": {"sumHrs":12974.09,"orders":27847,"delivTime":21.62,"rat":6.38,"toVendor":3.27,"onTime":0.88,"failRate":0.0209},
    "Ain shams":  {"sumHrs":2335.00, "orders":4573, "delivTime":23.14,"rat":6.69,"toVendor":4.13,"onTime":0.77,"failRate":0.0318},
}
tableau_wtd = {
    "Nasr city":  {"sumHrs":14082.03,"orders":28598,"delivTime":25.14,"rat":6.84,"toVendor":3.28,"onTime":0.85,"failRate":0.0246},
    "Heliopolis": {"sumHrs":12974.09,"orders":27854,"delivTime":24.33,"rat":6.38,"toVendor":3.27,"onTime":0.88,"failRate":0.0209},
    "Ain shams":  {"sumHrs":2335.00, "orders":4573, "delivTime":26.84,"rat":6.69,"toVendor":4.13,"onTime":0.77,"failRate":0.0318},
}
tableau_mtd = {
    "Nasr city":  {"sumHrs":201919.44,"orders":421259,"delivTime":26.4,"rat":7.83,"toVendor":3.40,"onTime":0.84,"failRate":0.0275},
    "Heliopolis": {"sumHrs":181999.45,"orders":394417,"delivTime":25.7,"rat":7.52,"toVendor":3.29,"onTime":0.8521,"failRate":0.0241},
    "Ain shams":  {"sumHrs":34744.04, "orders":69431, "delivTime":26.73,"rat":6.37,"toVendor":3.99,"onTime":0.795,"failRate":0.059},
}

# ── Looker shift data ─────────────────────────────────────────────────────────
shift_yday = {
    "Nasr city":  {"plannedHrs":16782.08,"lateLogin":0.0389,"breakMin":59.52,"acceptRate":0.8583},
    "Heliopolis": {"plannedHrs":15547.26,"lateLogin":0.0472,"breakMin":49.63,"acceptRate":0.8454},
    "Ain shams":  {"plannedHrs":2884.84, "lateLogin":0.0333,"breakMin":33.85,"acceptRate":0.8397},
}
shift_wtd = shift_yday  # WTD = yday (Monday)
shift_mtd = {
    "Nasr city":  {"plannedHrs":220093.48,"lateLogin":0.0569,"breakMin":57.29,"acceptRate":0.8515},
    "Heliopolis": {"plannedHrs":205480.14,"lateLogin":0.0591,"breakMin":55.41,"acceptRate":0.823},
    "Ain shams":  {"plannedHrs":39575.93, "lateLogin":0.0623,"breakMin":40.31,"acceptRate":0.8206},
}
ns_yday = {
    "Nasr city":  {"noShow":0.0274,"riders":1635},
    "Heliopolis": {"noShow":0.0507,"riders":1618},
    "Ain shams":  {"noShow":0.0583,"riders":331},
}
ns_wtd = ns_yday  # WTD = yday
ns_mtd = {
    "Nasr city":  {"noShow":0.0304,"riders":2726},
    "Heliopolis": {"noShow":0.0547,"riders":2803},
    "Ain shams":  {"noShow":0.0439,"riders":602},
}

# ── Run rates ─────────────────────────────────────────────────────────────────
sheet_rr = {
    "yday": {"Nasr city":0.9504,"Heliopolis":0.8666,"Ain shams":0.8833},
    "wtd":  {"Nasr city":0.995, "Heliopolis":0.961, "Ain shams":0.921},
    "mtd":  {"Nasr city":0.995, "Heliopolis":0.9611,"Ain shams":0.9206},
}

# ── DTC ───────────────────────────────────────────────────────────────────────
dtc_yday = {
    "ard_golf":[75,0,0],"hegaz":[57,0,0],"matareya":[45,0,0],
    "hadeeqa":[82,0,0],"tayaran":[51,0,0],"hay8":[46,0,0],
    "shorouk":[78,0,0],"masaken_sh":[54,0,0],"omarat":[49,0,0]
}
dtc_mtd = {
    "ard_golf":[80,0,0],"hegaz":[56.4,0,0],"matareya":[34.4,0,0],
    "hadeeqa":[81.1,0,0],"tayaran":[53,0,0],"hay8":[27.6,0,0],
    "shorouk":[73.2,0,0],"masaken_sh":[48.6,0,0],"omarat":[44.4,0,0]
}

# ── Zone object builder ───────────────────────────────────────────────────────
def zone_obj(tab, shift, ns, rr=None):
    sumHrs = tab['sumHrs']
    orders = tab['orders']
    riders = ns['riders']
    utr    = r4(orders / sumHrs) if sumHrs else 0
    avgHrs = r4(sumHrs / riders) if riders else 0
    fill   = shift['acceptRate']
    obj = {
        "riders":    riders,
        "orders":    orders,
        "sumHrs":    r2(sumHrs),
        "plannedHrs":r2(shift['plannedHrs']),
        "lateLogin": r4(shift['lateLogin']),
        "noShow":    r4(ns['noShow']),
        "breakMin":  r2(shift['breakMin']),
        "fill":      r4(fill),
        "acceptRate":r4(fill),
        "delivTime": r4(tab['delivTime']),
        "rat":       r4(tab['rat']),
        "toVendor":  r4(tab['toVendor']),
        "onTime":    r4(tab['onTime']),
        "failRate":  r4(tab['failRate']),
    }
    if rr is not None:
        obj['rr'] = rr
    return obj

# ── Read Looker raw data (written by browser) ─────────────────────────────────
with open('/tmp/ncops/looker_data.json') as f:
    ld = json.load(f)

# ── Section C: Offenders ──────────────────────────────────────────────────────
offenders = {"Nasr city":[], "Heliopolis":[], "Ain shams":[]}
for row in ld.get('offRaw', []):
    zone = row.get('dim_logistics_rider.last_operating_zone_name','')
    if zone not in offenders: continue
    act  = row.get('agg_logistics_rider_performance.sum_actual_working_duration',0) or 0
    plan = row.get('agg_logistics_rider_performance.sum_planned_working_duration',0) or 1
    brk  = row.get('agg_logistics_rider_performance.sum_breaking_duration',0) or 0
    shifts = row.get('agg_logistics_rider_performance.all_shifts',0) or 0
    offenders[zone].append({
        "id":    int(row.get('agg_logistics_rider_performance.rider_id',0)),
        "noShow":int(row.get('agg_logistics_rider_performance.no_show_shifts',0)),
        "late":  int(row.get('agg_logistics_rider_performance.late_login_shifts',0)),
        "breaks":round(brk/60, 1),
        "avp":   round((act/plan)*100, 1) if plan > 0 else 0,
        "shifts":int(shifts),
    })

# ── Section E: Hybrid SPs ─────────────────────────────────────────────────────
def build_hybrid(e1rows, e1brows):
    out = {}
    # E1: riders, actHrs, planHrs, noShow
    for row in (e1rows or []):
        sp = str(row.get('dim_logistics_rider.starting_points_ids',''))
        if not sp: continue
        out[sp] = {
            "riders":  int(row.get('agg_logistics_rider_performance.total_active_riders',0)),
            "actHrs":  r2(row.get('agg_logistics_rider_performance.sum_actual_working_duration',0)),
            "planHrs": r2(row.get('agg_logistics_rider_performance.sum_planned_working_duration',0)),
            "noShow":  r4(row.get('agg_logistics_rider_performance.no_show_percentage',0)),
        }
    # E1b: lateLogin
    for row in (e1brows or []):
        sp = str(int(row.get('fct_logistics_rider_shift.sp_id',0)))
        if sp in out:
            out[sp]['lateLogin'] = r4(row.get('fct_logistics_rider_shift.late_10_shifts_Percentage',0))
    # Fill missing with defaults
    for sp in out:
        if 'lateLogin' not in out[sp]: out[sp]['lateLogin'] = 0
    return out

# Load existing hybrid for order-based metrics (E2 timed out)
with open('/tmp/ncops/dashboard_data.json') as f:
    existing = json.load(f)

def merge_hybrid(new_e1, existing_period):
    """Merge E1 data with existing E2 metrics (orders/dt/rat etc)"""
    out = {}
    for sp, vals in new_e1.items():
        ex = existing_period.get(sp, {})
        out[sp] = {
            **vals,
            "orders": ex.get('orders', 0),
            "dt":     ex.get('dt', 0),
            "rat":    ex.get('rat', 0),
            "tv":     ex.get('tv', 0),
            "tc":     ex.get('tc', 0),
            "onTime": ex.get('onTime', 0),
        }
    return out

hybrid_yday_e1 = build_hybrid(ld.get('e1yd',[]), ld.get('e1byd',[]))
hybrid_mtd_e1  = build_hybrid(ld.get('e1mtd',[]), ld.get('e1bmtd',[]))
# WTD = yday for SPs too
hybrid_yday = merge_hybrid(hybrid_yday_e1, existing['hybrid']['yday'])
hybrid_wtd  = merge_hybrid(hybrid_yday_e1, existing['hybrid']['wtd'])
hybrid_mtd  = merge_hybrid(hybrid_mtd_e1,  existing['hybrid']['mtd'])

# ── Section F: Tmart perf ─────────────────────────────────────────────────────
def build_perf(rows, skip_ot=False):
    out = {}
    for row in (rows or []):
        vc = str(row.get('fct_logistics_order.vendor_code',''))
        if not vc: continue
        obj = {
            "orders_total": int(row.get('fct_logistics_order.orders_total',0) or 0),
            "dt":  r4(row.get('fct_logistics_order.avg_delivery_time',0) or 0),
            "rat": r4(row.get('fct_logistics_order.Avg_Rider_Accepting_Time',0) or 0),
            "tv":  r4(row.get('fct_logistics_order.avg_to_vendor_time',0) or 0),
            "tc":  r4(row.get('fct_logistics_order.tc',0) or 0),
            "avtc":r4(row.get('fct_logistics_order.avtc',0) or 0),
            "l10": r4(row.get('fct_logistics_order.l10',0) or 0),
            "l5":  r4(row.get('fct_logistics_order.l5',0) or 0),
        }
        if not skip_ot:
            obj['ot']  = r4(row.get('fct_logistics_order.Pct_Order_On_Time',0) or 0)
            obj['fir'] = r4(row.get('fct_logistics_order.fir',0) or 0)
        out[vc] = obj
    return out

perf_yday = build_perf(ld.get('fyd',[]))
perf_l3d  = build_perf(ld.get('fl3',[]))
perf_l7d  = build_perf(ld.get('fl7',[]))
perf_mtd  = build_perf(ld.get('fmtd',[]))
perf_lm   = build_perf(ld.get('flm',[]), skip_ot=True)
# l14d = carry forward existing
perf_l14d = existing['perf'].get('l14d', {})
# Carry existing lm ot/fir
for vc, ex in existing['perf'].get('lm', {}).items():
    if vc in perf_lm:
        perf_lm[vc]['ot']  = ex.get('ot', 0)
        perf_lm[vc]['fir'] = ex.get('fir', 0)

# perf_shift (carry forward existing — needs lateLogin from SP queries not run)
perf_shift = existing.get('perf_shift', {})

# ── 3PL aggregation ───────────────────────────────────────────────────────────
def agg_3pl(rows):
    m = {}
    for r in (rows or []):
        cn = (r.get('agg_logistics_rider_performance.contract_name','') or '').strip()
        if not cn: continue
        zone = r.get('dim_logistics_rider.last_operating_zone_name','')
        k = f"{zone}|{cn}"
        if k not in m: m[k] = {'hrs':0,'riders':0,'days':set()}
        m[k]['hrs']    += r.get('agg_logistics_rider_performance.sum_actual_working_duration',0) or 0
        m[k]['riders'] += r.get('agg_logistics_rider_performance.total_active_riders',0) or 0
        m[k]['days'].add(r.get('agg_logistics_rider_performance.created_date_date',''))
    return m

agg_yd  = agg_3pl(ld.get('pl_yd',[]))
agg_w7  = agg_3pl(ld.get('pl_w7',[]))
agg_mtd = agg_3pl(ld.get('pl_mtd',[]))
agg_lm  = agg_3pl(ld.get('pl_lm',[]))

# Verify yday date
yd_dates = set(r.get('agg_logistics_rider_performance.created_date_date','') for r in ld.get('pl_yd',[]))
print(f"3PL yday dates: {yd_dates}")

def awh(hrs, riders): return r2(hrs/riders) if riders > 0 else 0

TLP_YDAY = {}; TLP_W7 = {}; TLP_MTD = {}; TLP_MONTH = {}
TLP_RIDERS_YDAY = {}; TLP_RIDERS_MTD_SUM = {}
TLP_AWH_YDAY = {}; TLP_AWH_W7 = {}; TLP_AWH_MTD = {}; TLP_AWH_MONTH = {}

for k in set(list(agg_yd.keys()) + list(agg_w7.keys()) + list(agg_mtd.keys()) + list(agg_lm.keys())):
    yh = agg_yd.get(k,{}).get('hrs',0)
    yr = agg_yd.get(k,{}).get('riders',0)
    wh = agg_w7.get(k,{}).get('hrs',0)
    wr = agg_w7.get(k,{}).get('riders',0)
    mh = agg_mtd.get(k,{}).get('hrs',0)
    mr = agg_mtd.get(k,{}).get('riders',0)
    oh = agg_lm.get(k,{}).get('hrs',0)
    or_ = agg_lm.get(k,{}).get('riders',0)
    TLP_YDAY[k]            = r2(yh)
    TLP_W7[k]              = r2(wh / 7)
    TLP_MTD[k]             = r2(mh / MTD_DAYS)
    TLP_MONTH[k]           = r2(oh / LM_DAYS)
    TLP_RIDERS_YDAY[k]     = int(yr)
    TLP_RIDERS_MTD_SUM[k]  = int(mr)
    TLP_AWH_YDAY[k]        = awh(yh, yr)
    TLP_AWH_W7[k]          = awh(wh, wr)
    TLP_AWH_MTD[k]         = awh(mh, mr / MTD_DAYS if MTD_DAYS else 1)
    TLP_AWH_MONTH[k]       = awh(oh, or_ / LM_DAYS if LM_DAYS else 1)

# ── Assemble final data ───────────────────────────────────────────────────────
yday_label = f"{MONTHS[yday.month-1]} {yday.day}, {yday.year}"
wk_num = yday.isocalendar()[1]

data = {
    "generated": today.strftime('%Y-%m-%d'),
    "data_date":  yday.strftime('%Y-%m-%d'),
    "zone": {
        "yday": {
            "label": yday_label,
            "Nasr city":  zone_obj(tableau_yday["Nasr city"],  shift_yday["Nasr city"],  ns_yday["Nasr city"],  rr=sheet_rr["yday"]["Nasr city"]),
            "Heliopolis": zone_obj(tableau_yday["Heliopolis"], shift_yday["Heliopolis"], ns_yday["Heliopolis"], rr=sheet_rr["yday"]["Heliopolis"]),
            "Ain shams":  zone_obj(tableau_yday["Ain shams"],  shift_yday["Ain shams"],  ns_yday["Ain shams"],  rr=sheet_rr["yday"]["Ain shams"]),
        },
        "wtd": {
            "label": f"Wk {wk_num}  {MONTHS[week_start.month-1]} {week_start.day}-{yday.day}",
            "short": f"Wk {wk_num}",
            "Nasr city":  zone_obj(tableau_wtd["Nasr city"],  shift_wtd["Nasr city"],  ns_wtd["Nasr city"],  rr=sheet_rr["wtd"]["Nasr city"]),
            "Heliopolis": zone_obj(tableau_wtd["Heliopolis"], shift_wtd["Heliopolis"], ns_wtd["Heliopolis"], rr=sheet_rr["wtd"]["Heliopolis"]),
            "Ain shams":  zone_obj(tableau_wtd["Ain shams"],  shift_wtd["Ain shams"],  ns_wtd["Ain shams"],  rr=sheet_rr["wtd"]["Ain shams"]),
        },
        "mtd": {
            "label": f"{MONTHS[yday.month-1]} {yday.year} (MTD {MONTHS[yday.month-1]} 1-{yday.day})",
            "Nasr city":  zone_obj(tableau_mtd["Nasr city"],  shift_mtd["Nasr city"],  ns_mtd["Nasr city"],  rr=sheet_rr["mtd"]["Nasr city"]),
            "Heliopolis": zone_obj(tableau_mtd["Heliopolis"], shift_mtd["Heliopolis"], ns_mtd["Heliopolis"], rr=sheet_rr["mtd"]["Heliopolis"]),
            "Ain shams":  zone_obj(tableau_mtd["Ain shams"],  shift_mtd["Ain shams"],  ns_mtd["Ain shams"],  rr=sheet_rr["mtd"]["Ain shams"]),
        },
    },
    "dtc_yday": dtc_yday,
    "dtc_mtd":  dtc_mtd,
    "offenders": offenders,
    "hybrid":    {"yday": hybrid_yday, "wtd": hybrid_wtd, "mtd": hybrid_mtd},
    "perf":      {"yday":perf_yday,"l3d":perf_l3d,"l7d":perf_l7d,"l14d":perf_l14d,"mtd":perf_mtd,"lm":perf_lm},
    "perf_shift": perf_shift,
    "tlp_yday":   TLP_YDAY,
    "tlp_w7":     TLP_W7,
    "tlp_mtd":    TLP_MTD,
    "tlp_month":  TLP_MONTH,
    "tlp_riders_yday": TLP_RIDERS_YDAY,
    "tlp_riders_mtd_sum": TLP_RIDERS_MTD_SUM,
    "tlp_awh_yday":  TLP_AWH_YDAY,
    "tlp_awh_w7":    TLP_AWH_W7,
    "tlp_awh_mtd":   TLP_AWH_MTD,
    "tlp_awh_month": TLP_AWH_MONTH,
}

with open('/tmp/ncops/dashboard_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("dashboard_data.json written")
print(f"Zones yday: {list(data['zone']['yday'].keys())}")
print(f"Offenders: Nasr city={len(offenders['Nasr city'])}, Helio={len(offenders['Heliopolis'])}, Ain shams={len(offenders['Ain shams'])}")
print(f"Perf vendors yday: {sorted(perf_yday.keys())}")
print(f"3PL keys (yday): {sorted(list(TLP_YDAY.keys()))[:5]}")
