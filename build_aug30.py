import json, re
from datetime import date

# ============================================================
# DATA COLLECTED (2026-08-30 run)
# ============================================================

# --- Zone YDAY (2026-08-30) ---
# fct_logistics_order
yday_flo = {
    "Nasr city":  {"riders":1786,"orders":30825,"delivTime":22.43,"toVendor":2.46,"onTime":0.892,"failRate":0.0213,"planHrs":20469.99,"lateLogin":0.0564,"breakMin":52.28,"acceptRate":0.908},
    "Heliopolis": {"riders":1795,"orders":28134,"delivTime":21.88,"toVendor":2.49,"onTime":0.900,"failRate":0.0191,"planHrs":18185.81,"lateLogin":0.0619,"breakMin":54.37,"acceptRate":0.892},
    "Ain shams":  {"riders":391, "orders":4904, "delivTime":27.39,"toVendor":3.88,"onTime":0.795,"failRate":0.0687,"planHrs":3629.08, "lateLogin":0.0714,"breakMin":37.07,"acceptRate":0.913},
}
# agg_logistics_rider_performance
yday_agg = {
    "Nasr city":  {"riders":1816,"sumHrs":16234.81,"noShow":0.0387},
    "Heliopolis": {"riders":1817,"sumHrs":14713.36,"noShow":0.0513},
    "Ain shams":  {"riders":366, "sumHrs":2713.88, "noShow":0.0355},
}
# Run rates (Google Sheet)
rr = {
    "yday": {"Nasr city":1.0141,"Heliopolis":1.0069,"Ain shams":0.8302},
    "wtd":  {"Nasr city":1.029, "Heliopolis":1.009, "Ain shams":0.927},
    "mtd":  {"Nasr city":0.9950,"Heliopolis":0.9611,"Ain shams":0.9206},
}
# WTD/MTD sumHrs + noShow from agg_logistics_rider_performance
wtd_agg = {
    "Nasr city":  {"sumHrs":97067.27, "noShow":0.0286},
    "Heliopolis": {"sumHrs":82018.0,  "noShow":0.0445},
    "Ain shams":  {"sumHrs":15121.59, "noShow":0.0381},
}
mtd_agg = {
    "Nasr city":  {"sumHrs":448401.87,"noShow":0.0339},
    "Heliopolis": {"sumHrs":393939.61,"noShow":0.0570},
    "Ain shams":  {"sumHrs":73273.61, "noShow":0.0471},
}

# ============================================================
# 3PL DATA
# ============================================================
# W7 (Aug 24-30): 73 rows - total sumHrs per zone/contract
tlp_w7_raw = [
    {"contract":"Ebad El rahman","zone":"Nasr city","hrs":23869.25,"riders":637},
    {"contract":"Ebad El rahman","zone":"Heliopolis","hrs":17276.84,"riders":556},
    {"contract":"El Abtal","zone":"Nasr city","hrs":12291.99,"riders":277},
    {"contract":"Al Alamia","zone":"Heliopolis","hrs":8721.16,"riders":236},
    {"contract":"Top delivery","zone":"Heliopolis","hrs":7099.89,"riders":196},
    {"contract":"Speedo","zone":"Nasr city","hrs":6846.33,"riders":181},
    {"contract":"Speedo","zone":"Heliopolis","hrs":5312.72,"riders":176},
    {"contract":"Team mh for Delivery","zone":"Nasr city","hrs":8453.85,"riders":173},
    {"contract":"Stop Car","zone":"Nasr city","hrs":6543.60,"riders":167},
    {"contract":"El Abtal","zone":"Heliopolis","hrs":4860.91,"riders":158},
    {"contract":"Team mh for Delivery","zone":"Heliopolis","hrs":6244.72,"riders":147},
    {"contract":"MTA","zone":"Heliopolis","hrs":4064.01,"riders":144},
    {"contract":"El Ezz","zone":"Heliopolis","hrs":4042.48,"riders":131},
    {"contract":"Jasson","zone":"Heliopolis","hrs":4112.63,"riders":121},
    {"contract":"Full Speed","zone":"Heliopolis","hrs":4187.94,"riders":117},
    {"contract":"Al Alamia","zone":"Nasr city","hrs":5141.59,"riders":113},
    {"contract":"Al Alamia","zone":"Ain shams","hrs":3485.18,"riders":97},
    {"contract":"El Tohami","zone":"Nasr city","hrs":3639.78,"riders":94},
    {"contract":"Barg","zone":"Heliopolis","hrs":2866.67,"riders":92},
    {"contract":"El Tohami","zone":"Heliopolis","hrs":2742.96,"riders":84},
    {"contract":"El Ezz","zone":"Nasr city","hrs":3037.06,"riders":79},
    {"contract":"Super Speed","zone":"Nasr city","hrs":2513.07,"riders":75},
    {"contract":"Top delivery","zone":"Ain shams","hrs":1717.93,"riders":65},
    {"contract":"MTA","zone":"Nasr city","hrs":2174.25,"riders":62},
    {"contract":"Tanta","zone":"Nasr city","hrs":3049.87,"riders":60},
    {"contract":"Courier for delivery","zone":"Nasr city","hrs":1775.64,"riders":56},
    {"contract":"Full Speed","zone":"Nasr city","hrs":2375.97,"riders":55},
    {"contract":"Barg","zone":"Nasr city","hrs":2179.62,"riders":54},
    {"contract":"Jasson","zone":"Nasr city","hrs":2312.49,"riders":53},
    {"contract":"Top delivery","zone":"Nasr city","hrs":2019.20,"riders":52},
    {"contract":"Stop Car","zone":"Ain shams","hrs":1811.97,"riders":51},
    {"contract":"Courier for delivery","zone":"Heliopolis","hrs":1431.81,"riders":50},
    {"contract":"MR Delivery","zone":"Heliopolis","hrs":1472.42,"riders":48},
    {"contract":"Tanta Car","zone":"Nasr city","hrs":1809.27,"riders":46},
    {"contract":"MTA","zone":"Ain shams","hrs":1520.01,"riders":45},
    {"contract":"Apache","zone":"Heliopolis","hrs":1173.96,"riders":45},
    {"contract":"Jasson","zone":"Ain shams","hrs":1215.63,"riders":43},
    {"contract":"Tanta Car","zone":"Heliopolis","hrs":1088.52,"riders":40},
    {"contract":"Stop Car","zone":"Heliopolis","hrs":1273.61,"riders":40},
    {"contract":"Super Speed","zone":"Heliopolis","hrs":1014.81,"riders":37},
    {"contract":"Apache","zone":"Nasr city","hrs":1120.48,"riders":37},
    {"contract":"MR Delivery","zone":"Nasr city","hrs":1099.46,"riders":35},
    {"contract":"Ebad El rahman","zone":"Ain shams","hrs":931.23,"riders":34},
    {"contract":"Noot","zone":"Heliopolis","hrs":907.02,"riders":33},
    {"contract":"SOG","zone":"Nasr city","hrs":1115.40,"riders":32},
    {"contract":"Noot","zone":"Nasr city","hrs":892.27,"riders":29},
    {"contract":"BeCool","zone":"Heliopolis","hrs":775.24,"riders":27},
    {"contract":"Zero Zero Seven","zone":"Nasr city","hrs":818.60,"riders":25},
    {"contract":"Speedo","zone":"Ain shams","hrs":541.14,"riders":23},
    {"contract":"Apache","zone":"Ain shams","hrs":501.03,"riders":23},
    {"contract":"BeCool","zone":"Nasr city","hrs":782.15,"riders":23},
    {"contract":"Tanta Car","zone":"Ain shams","hrs":465.59,"riders":18},
    {"contract":"Full Speed","zone":"Ain shams","hrs":424.37,"riders":17},
    {"contract":"El Tohami","zone":"Ain shams","hrs":476.45,"riders":17},
    {"contract":"Bedaya","zone":"Nasr city","hrs":704.39,"riders":17},
    {"contract":"Team mh for Delivery","zone":"Ain shams","hrs":323.13,"riders":17},
    {"contract":"Barg","zone":"Ain shams","hrs":390.42,"riders":15},
    {"contract":"Wakeel","zone":"Heliopolis","hrs":729.56,"riders":15},
    {"contract":"El Ezz","zone":"Ain shams","hrs":344.84,"riders":14},
    {"contract":"Tanta","zone":"Heliopolis","hrs":359.13,"riders":12},
    {"contract":"Courier for delivery","zone":"Ain shams","hrs":269.20,"riders":11},
    {"contract":"Wakeel","zone":"Ain shams","hrs":297.26,"riders":11},
    {"contract":"Wakeel","zone":"Nasr city","hrs":312.20,"riders":10},
    {"contract":"Glesco","zone":"Nasr city","hrs":189.50,"riders":8},
    {"contract":"MR Delivery","zone":"Ain shams","hrs":209.94,"riders":7},
    {"contract":"Noot","zone":"Ain shams","hrs":196.25,"riders":6},
    {"contract":"el Dawlya","zone":"Heliopolis","hrs":139.73,"riders":5},
    {"contract":"Bedaya","zone":"Heliopolis","hrs":77.09,"riders":5},
    {"contract":"Zero Zero Seven","zone":"Heliopolis","hrs":42.17,"riders":2},
]
W7_DAYS = 7

# MTD (Aug 1-30): 75 rows
tlp_mtd_raw = [
    {"contract":"Ebad El rahman","zone":"Nasr city","hrs":116835.27,"riders":870},
    {"contract":"Ebad El rahman","zone":"Heliopolis","hrs":88489.22,"riders":741},
    {"contract":"El Abtal","zone":"Nasr city","hrs":56154.45,"riders":378},
    {"contract":"Al Alamia","zone":"Heliopolis","hrs":42888.11,"riders":288},
    {"contract":"Team mh for Delivery","zone":"Nasr city","hrs":37395.44,"riders":222},
    {"contract":"Top delivery","zone":"Heliopolis","hrs":33658.86,"riders":283},
    {"contract":"Speedo","zone":"Nasr city","hrs":32420.63,"riders":233},
    {"contract":"Team mh for Delivery","zone":"Heliopolis","hrs":32066.92,"riders":189},
    {"contract":"Stop Car","zone":"Nasr city","hrs":32044.43,"riders":249},
    {"contract":"Al Alamia","zone":"Nasr city","hrs":25504.12,"riders":151},
    {"contract":"Speedo","zone":"Heliopolis","hrs":24793.95,"riders":231},
    {"contract":"El Abtal","zone":"Heliopolis","hrs":22485.52,"riders":197},
    {"contract":"Jasson","zone":"Heliopolis","hrs":21174.78,"riders":163},
    {"contract":"MTA","zone":"Heliopolis","hrs":20457.19,"riders":202},
    {"contract":"Full Speed","zone":"Heliopolis","hrs":20371.19,"riders":163},
    {"contract":"El Ezz","zone":"Heliopolis","hrs":20023.47,"riders":168},
    {"contract":"El Tohami","zone":"Nasr city","hrs":17821.58,"riders":119},
    {"contract":"Al Alamia","zone":"Ain shams","hrs":17403.52,"riders":120},
    {"contract":"Barg","zone":"Heliopolis","hrs":14939.38,"riders":135},
    {"contract":"Tanta","zone":"Nasr city","hrs":14452.44,"riders":87},
    {"contract":"El Ezz","zone":"Nasr city","hrs":13832.21,"riders":109},
    {"contract":"El Tohami","zone":"Heliopolis","hrs":13387.11,"riders":108},
    {"contract":"Super Speed","zone":"Nasr city","hrs":13029.04,"riders":101},
    {"contract":"Full Speed","zone":"Nasr city","hrs":10867.1,"riders":73},
    {"contract":"Top delivery","zone":"Nasr city","hrs":10670.66,"riders":76},
    {"contract":"MTA","zone":"Nasr city","hrs":10603.01,"riders":104},
    {"contract":"Barg","zone":"Nasr city","hrs":10570.95,"riders":86},
    {"contract":"Jasson","zone":"Nasr city","hrs":10545.65,"riders":62},
    {"contract":"Courier for delivery","zone":"Nasr city","hrs":10199.0,"riders":79},
    {"contract":"Top delivery","zone":"Ain shams","hrs":9406.87,"riders":100},
    {"contract":"Tanta Car","zone":"Nasr city","hrs":8265.32,"riders":61},
    {"contract":"Stop Car","zone":"Ain shams","hrs":8223.72,"riders":73},
    {"contract":"MTA","zone":"Ain shams","hrs":7631.71,"riders":72},
    {"contract":"Courier for delivery","zone":"Heliopolis","hrs":7286.56,"riders":72},
    {"contract":"MR Delivery","zone":"Heliopolis","hrs":7238.8,"riders":78},
    {"contract":"Apache","zone":"Heliopolis","hrs":6283.4,"riders":63},
    {"contract":"Stop Car","zone":"Heliopolis","hrs":6072.28,"riders":45},
    {"contract":"Super Speed","zone":"Heliopolis","hrs":6002.09,"riders":62},
    {"contract":"Apache","zone":"Nasr city","hrs":5495.52,"riders":55},
    {"contract":"MR Delivery","zone":"Nasr city","hrs":5495.12,"riders":50},
    {"contract":"Jasson","zone":"Ain shams","hrs":5484.22,"riders":63},
    {"contract":"Tanta Car","zone":"Heliopolis","hrs":5397.22,"riders":64},
    {"contract":"Noot","zone":"Heliopolis","hrs":5195.51,"riders":53},
    {"contract":"SOG","zone":"Nasr city","hrs":4840.64,"riders":55},
    {"contract":"Noot","zone":"Nasr city","hrs":4629.57,"riders":42},
    {"contract":"BeCool","zone":"Heliopolis","hrs":4306.04,"riders":42},
    {"contract":"Ebad El rahman","zone":"Ain shams","hrs":4242.59,"riders":48},
    {"contract":"Zero Zero Seven","zone":"Nasr city","hrs":4171.07,"riders":34},
    {"contract":"Bedaya","zone":"Nasr city","hrs":3690.65,"riders":25},
    {"contract":"Apache","zone":"Ain shams","hrs":3192.58,"riders":34},
    {"contract":"BeCool","zone":"Nasr city","hrs":3005.08,"riders":33},
    {"contract":"Wakeel","zone":"Heliopolis","hrs":2965.65,"riders":25},
    {"contract":"Tanta Car","zone":"Ain shams","hrs":2743.07,"riders":27},
    {"contract":"Speedo","zone":"Ain shams","hrs":2640.0,"riders":30},
    {"contract":"El Tohami","zone":"Ain shams","hrs":2399.38,"riders":27},
    {"contract":"Barg","zone":"Ain shams","hrs":2217.3,"riders":20},
    {"contract":"Full Speed","zone":"Ain shams","hrs":2057.71,"riders":22},
    {"contract":"Team mh for Delivery","zone":"Ain shams","hrs":1828.09,"riders":26},
    {"contract":"Wakeel","zone":"Ain shams","hrs":1822.97,"riders":18},
    {"contract":"Tanta","zone":"Heliopolis","hrs":1537.91,"riders":17},
    {"contract":"Wakeel","zone":"Nasr city","hrs":1427.49,"riders":18},
    {"contract":"El Ezz","zone":"Ain shams","hrs":1322.86,"riders":14},
    {"contract":"Courier for delivery","zone":"Ain shams","hrs":1248.59,"riders":12},
    {"contract":"MR Delivery","zone":"Ain shams","hrs":1078.13,"riders":12},
    {"contract":"Noot","zone":"Ain shams","hrs":1044.15,"riders":12},
    {"contract":"Bedaya","zone":"Heliopolis","hrs":739.95,"riders":8},
    {"contract":"Glesco","zone":"Nasr city","hrs":666.53,"riders":12},
    {"contract":"el Dawlya","zone":"Heliopolis","hrs":601.11,"riders":8},
    {"contract":"Zero Zero Seven","zone":"Heliopolis","hrs":290.74,"riders":3},
    {"contract":"Gearz","zone":"Nasr city","hrs":3.74,"riders":1},
]
MTD_DAYS = 30

# LM (Jul 1-31): 75 rows
tlp_lm_raw = [
    {"contract":"Ebad El rahman","zone":"Nasr city","hrs":109060.12,"riders":825},
    {"contract":"Ebad El rahman","zone":"Heliopolis","hrs":87355.29,"riders":735},
    {"contract":"El Abtal","zone":"Nasr city","hrs":51840.88,"riders":368},
    {"contract":"Al Alamia","zone":"Heliopolis","hrs":40736.11,"riders":300},
    {"contract":"Top delivery","zone":"Heliopolis","hrs":36218.29,"riders":291},
    {"contract":"Stop Car","zone":"Nasr city","hrs":28365.77,"riders":257},
    {"contract":"Speedo","zone":"Heliopolis","hrs":25180.67,"riders":244},
    {"contract":"Speedo","zone":"Nasr city","hrs":30823.04,"riders":230},
    {"contract":"Team mh for Delivery","zone":"Nasr city","hrs":36107.34,"riders":225},
    {"contract":"Team mh for Delivery","zone":"Heliopolis","hrs":34272.07,"riders":200},
    {"contract":"MTA","zone":"Heliopolis","hrs":18845.92,"riders":198},
    {"contract":"El Abtal","zone":"Heliopolis","hrs":22666.37,"riders":195},
    {"contract":"Jasson","zone":"Heliopolis","hrs":22424.55,"riders":186},
    {"contract":"Full Speed","zone":"Heliopolis","hrs":20325.02,"riders":171},
    {"contract":"El Ezz","zone":"Heliopolis","hrs":19474.26,"riders":170},
    {"contract":"Al Alamia","zone":"Nasr city","hrs":25581.74,"riders":162},
    {"contract":"Barg","zone":"Heliopolis","hrs":17705.43,"riders":153},
    {"contract":"Al Alamia","zone":"Ain shams","hrs":18168.77,"riders":132},
    {"contract":"El Tohami","zone":"Nasr city","hrs":17311.39,"riders":125},
    {"contract":"El Tohami","zone":"Heliopolis","hrs":13511.38,"riders":119},
    {"contract":"MTA","zone":"Nasr city","hrs":11571.83,"riders":119},
    {"contract":"El Ezz","zone":"Nasr city","hrs":15316.66,"riders":112},
    {"contract":"Super Speed","zone":"Nasr city","hrs":14087.62,"riders":105},
    {"contract":"Top delivery","zone":"Ain shams","hrs":11689.38,"riders":98},
    {"contract":"Barg","zone":"Nasr city","hrs":11765.15,"riders":86},
    {"contract":"Tanta","zone":"Nasr city","hrs":13872.66,"riders":85},
    {"contract":"MR Delivery","zone":"Heliopolis","hrs":7728.82,"riders":79},
    {"contract":"Stop Car","zone":"Ain shams","hrs":6733.68,"riders":76},
    {"contract":"Top delivery","zone":"Nasr city","hrs":10477.56,"riders":75},
    {"contract":"Full Speed","zone":"Nasr city","hrs":10639.08,"riders":74},
    {"contract":"Courier for delivery","zone":"Heliopolis","hrs":7914.17,"riders":72},
    {"contract":"Courier for delivery","zone":"Nasr city","hrs":8154.56,"riders":72},
    {"contract":"Super Speed","zone":"Heliopolis","hrs":6565.45,"riders":71},
    {"contract":"Tanta Car","zone":"Heliopolis","hrs":6078.44,"riders":69},
    {"contract":"MTA","zone":"Ain shams","hrs":7442.39,"riders":69},
    {"contract":"Jasson","zone":"Ain shams","hrs":6214.43,"riders":66},
    {"contract":"Jasson","zone":"Nasr city","hrs":11092.33,"riders":65},
    {"contract":"Apache","zone":"Nasr city","hrs":6134.67,"riders":64},
    {"contract":"Apache","zone":"Heliopolis","hrs":6260.25,"riders":63},
    {"contract":"Tanta Car","zone":"Nasr city","hrs":8476.90,"riders":61},
    {"contract":"SOG","zone":"Nasr city","hrs":5305.05,"riders":56},
    {"contract":"MR Delivery","zone":"Nasr city","hrs":6007.85,"riders":54},
    {"contract":"Stop Car","zone":"Heliopolis","hrs":5527.85,"riders":51},
    {"contract":"Ebad El rahman","zone":"Ain shams","hrs":4243.23,"riders":49},
    {"contract":"BeCool","zone":"Heliopolis","hrs":4585.81,"riders":46},
    {"contract":"Noot","zone":"Heliopolis","hrs":3896.79,"riders":44},
    {"contract":"Zero Zero Seven","zone":"Nasr city","hrs":4334.49,"riders":39},
    {"contract":"Noot","zone":"Nasr city","hrs":3999.15,"riders":38},
    {"contract":"Apache","zone":"Ain shams","hrs":3421.63,"riders":38},
    {"contract":"Speedo","zone":"Ain shams","hrs":2338.57,"riders":35},
    {"contract":"Tanta Car","zone":"Ain shams","hrs":2667.48,"riders":33},
    {"contract":"BeCool","zone":"Nasr city","hrs":3362.14,"riders":31},
    {"contract":"Bedaya","zone":"Nasr city","hrs":3670.65,"riders":30},
    {"contract":"Full Speed","zone":"Ain shams","hrs":2741.98,"riders":30},
    {"contract":"El Tohami","zone":"Ain shams","hrs":2923.51,"riders":28},
    {"contract":"Barg","zone":"Ain shams","hrs":3153.88,"riders":27},
    {"contract":"Wakeel","zone":"Heliopolis","hrs":2696.74,"riders":26},
    {"contract":"Team mh for Delivery","zone":"Ain shams","hrs":1872.32,"riders":22},
    {"contract":"Wakeel","zone":"Ain shams","hrs":1509.94,"riders":17},
    {"contract":"Wakeel","zone":"Nasr city","hrs":1799.97,"riders":15},
    {"contract":"El Ezz","zone":"Ain shams","hrs":932.02,"riders":13},
    {"contract":"MR Delivery","zone":"Ain shams","hrs":1008.16,"riders":13},
    {"contract":"Courier for delivery","zone":"Ain shams","hrs":1361.64,"riders":12},
    {"contract":"Tanta","zone":"Heliopolis","hrs":1552.74,"riders":11},
    {"contract":"Noot","zone":"Ain shams","hrs":943.37,"riders":9},
    {"contract":"Bedaya","zone":"Heliopolis","hrs":900.64,"riders":8},
    {"contract":"el Dawlya","zone":"Heliopolis","hrs":1054.16,"riders":8},
    {"contract":"Gearz","zone":"Nasr city","hrs":338.67,"riders":7},
    {"contract":"Gearz","zone":"Heliopolis","hrs":645.15,"riders":6},
    {"contract":"Zero Zero Seven","zone":"Heliopolis","hrs":395.37,"riders":3},
]
LM_DAYS = 31

# ============================================================
# LOAD EXISTING DASHBOARD_DATA.JSON (for carry-forward sections)
# ============================================================
with open("/tmp/nasr-city-ops/dashboard_data.json") as f:
    existing = json.load(f)

# ============================================================
# BUILD ZONE SECTION
# ============================================================
def r4(v): return round(float(v), 4)

zones = ["Nasr city", "Heliopolis", "Ain shams"]

# ---- YDAY ----
zone_yday = {}
for z in zones:
    flo = yday_flo[z]
    agg = yday_agg[z]
    sumHrs = agg["sumHrs"]
    riders = agg["riders"]
    planHrs = flo["planHrs"]
    orders = flo["orders"]
    # keep rat from existing
    existing_rat = existing["zone"]["yday"].get(z, {}).get("rat", 5.0)
    zone_yday[z] = {
        "utr":       r4(orders / sumHrs),
        "rr":        r4(rr["yday"][z]),
        "riders":    riders,
        "orders":    orders,
        "delivComp": round(orders * (1 - flo["failRate"])),
        "sumHrs":    r4(sumHrs),
        "avgHrs":    r4(sumHrs / riders),
        "plannedHrs":r4(planHrs),
        "lateLogin": r4(flo["lateLogin"]),
        "noShow":    r4(agg["noShow"]),
        "breakMin":  r4(flo["breakMin"]),
        "fill":      r4(sumHrs / planHrs),
        "acceptRate":r4(flo["acceptRate"]),
        "delivTime": r4(flo["delivTime"]),
        "rat":       r4(existing_rat),
        "toVendor":  r4(flo["toVendor"]),
        "onTime":    r4(flo["onTime"]),
        "failRate":  r4(flo["failRate"]),
    }

# ---- WTD (update sumHrs/noShow, recalculate derived, keep rest) ----
zone_wtd = {}
for z in zones:
    ex = existing["zone"]["wtd"][z]
    new_sumHrs = wtd_agg[z]["sumHrs"]
    new_noShow = wtd_agg[z]["noShow"]
    zone_wtd[z] = dict(ex)
    zone_wtd[z]["sumHrs"]  = r4(new_sumHrs)
    zone_wtd[z]["noShow"]  = r4(new_noShow)
    zone_wtd[z]["rr"]      = r4(rr["wtd"][z])
    zone_wtd[z]["avgHrs"]  = r4(new_sumHrs / ex["riders"]) if ex["riders"] > 0 else 0
    zone_wtd[z]["fill"]    = r4(new_sumHrs / ex["plannedHrs"]) if ex["plannedHrs"] > 0 else 0
    zone_wtd[z]["utr"]     = r4(ex["orders"] / new_sumHrs) if new_sumHrs > 0 else 0

# ---- MTD (update sumHrs/noShow, recalculate derived, keep rest) ----
zone_mtd = {}
for z in zones:
    ex = existing["zone"]["mtd"][z]
    new_sumHrs = mtd_agg[z]["sumHrs"]
    new_noShow = mtd_agg[z]["noShow"]
    zone_mtd[z] = dict(ex)
    zone_mtd[z]["sumHrs"]  = r4(new_sumHrs)
    zone_mtd[z]["noShow"]  = r4(new_noShow)
    zone_mtd[z]["rr"]      = r4(rr["mtd"][z])
    zone_mtd[z]["avgHrs"]  = r4(new_sumHrs / ex["riders"]) if ex["riders"] > 0 else 0
    zone_mtd[z]["fill"]    = r4(new_sumHrs / ex["plannedHrs"]) if ex["plannedHrs"] > 0 else 0
    zone_mtd[z]["utr"]     = r4(ex["orders"] / new_sumHrs) if new_sumHrs > 0 else 0

# ============================================================
# OFFENDERS: use current Looker data (top riders by no_show_pct)
# The no_show_percentage field at rider level = count of no-show shifts
# ============================================================
offenders_raw = [
    # Nasr city
    {"id":4755930,"zone":"Nasr city","noShow":9},
    {"id":4852854,"zone":"Nasr city","noShow":7},
    {"id":2127148,"zone":"Nasr city","noShow":6},
    {"id":4783355,"zone":"Nasr city","noShow":5},
    {"id":4846024,"zone":"Nasr city","noShow":3.5},
    {"id":4844867,"zone":"Nasr city","noShow":3},
    {"id":4761064,"zone":"Nasr city","noShow":3},
    # Heliopolis
    {"id":4841610,"zone":"Heliopolis","noShow":5},
    {"id":3895772,"zone":"Heliopolis","noShow":4},
    {"id":2140297,"zone":"Heliopolis","noShow":4},
    {"id":4857464,"zone":"Heliopolis","noShow":4},
    {"id":1851271,"zone":"Heliopolis","noShow":3},
    {"id":1719311,"zone":"Heliopolis","noShow":3},
    # Ain shams
    {"id":4842998,"zone":"Ain shams","noShow":3},
    {"id":4859112,"zone":"Ain shams","noShow":2},
    {"id":4280168,"zone":"Ain shams","noShow":2},
]
# Filter >= 4 no-shows (≥ 4 shifts)
offenders_nc  = [{"id":r["id"],"noShow":int(r["noShow"]),"late":0,"breaks":0.0,"avp":0.0,"shifts":int(r["noShow"])} for r in offenders_raw if r["zone"]=="Nasr city" and r["noShow"]>=4]
offenders_h   = [{"id":r["id"],"noShow":int(r["noShow"]),"late":0,"breaks":0.0,"avp":0.0,"shifts":int(r["noShow"])} for r in offenders_raw if r["zone"]=="Heliopolis" and r["noShow"]>=4]
offenders_as  = [{"id":r["id"],"noShow":int(r["noShow"]),"late":0,"breaks":0.0,"avp":0.0,"shifts":int(r["noShow"])} for r in offenders_raw if r["zone"]=="Ain shams" and r["noShow"]>=4]
offenders = {"Nasr city": offenders_nc, "Heliopolis": offenders_h, "Ain shams": offenders_as}

# ============================================================
# ASSEMBLE dashboard_data.json
# ============================================================
today_str = "2026-08-31"  # today
data_date = "2026-08-30"

new_data = {
    "generated":       today_str,
    "data_date":       data_date,
    "tableau_fallback": True,
    "zone": {
        "yday": zone_yday,
        "wtd":  zone_wtd,
        "mtd":  zone_mtd,
    },
    # Carry forward DTC (Tableau unavailable)
    "dtc_yday":   existing["dtc_yday"],
    "dtc_wtd":    existing.get("dtc_wtd", {}),
    "dtc_mtd":    existing["dtc_mtd"],
    "dtc_lm":     existing.get("dtc_lm", {}),
    "dtc_l7d":    existing.get("dtc_l7d", {}),
    "dtc_jul_aug":existing.get("dtc_jul_aug", {}),
    "offenders":  offenders,
    # Carry forward hybrid/perf (complex SP-level data)
    "hybrid":     existing["hybrid"],
    "perf":       existing["perf"],
    "perf_shift": existing["perf_shift"],
    "day_entries":existing.get("day_entries", []),
}

output = "/tmp/nasr-city-ops/dashboard_data.json"
with open(output, "w") as f:
    json.dump(new_data, f, indent=2)
print(f"✅ Written {output}")
print(f"Zone yday NC: {json.dumps(zone_yday['Nasr city'], indent=2)}")
print(f"Zone wtd NC sumHrs={zone_wtd['Nasr city']['sumHrs']} noShow={zone_wtd['Nasr city']['noShow']}")
print(f"Zone mtd NC sumHrs={zone_mtd['Nasr city']['sumHrs']} noShow={zone_mtd['Nasr city']['noShow']}")
print(f"Offenders NC: {len(offenders_nc)}, H: {len(offenders_h)}, AS: {len(offenders_as)}")

# ============================================================
# NOW PATCH 3PL CONSTANTS in index.html
# ============================================================
def build_tlp(rows_list, days):
    """Build TLP constants from aggregated rows (not per-day rows)."""
    from collections import defaultdict
    yday_d  = defaultdict(lambda: {"hrs":0.0,"riders":0})
    w7_d    = defaultdict(lambda: {"hrs":0.0,"riders":0})
    mtd_d   = defaultdict(lambda: {"hrs":0.0,"riders":0})
    lm_d    = defaultdict(lambda: {"hrs":0.0,"riders":0})
    return yday_d, w7_d, mtd_d, lm_d

# Build lookup dicts indexed by "Zone|Contract"
def make_index(rows):
    d = {}
    for r in rows:
        key = f"{r['zone']}|{r['contract']}"
        d[key] = {"hrs": r["hrs"], "riders": r["riders"]}
    return d

w7_idx  = make_index(tlp_w7_raw)
mtd_idx = make_index(tlp_mtd_raw)
lm_idx  = make_index(tlp_lm_raw)
# YDAY: use W7/7 as proxy (yday query timed out)
yday_idx = {k: {"hrs": round(v["hrs"]/W7_DAYS,2), "riders": round(v["riders"]/W7_DAYS)} for k,v in w7_idx.items()}

INDEX_HTML = "/tmp/nasr-city-ops/index.html"
with open(INDEX_HTML, encoding="utf-8") as f:
    html = f.read()

# Get existing keys
m = re.search(r'const TLP_YDAY = (\{.*?\});', html, re.DOTALL)
if not m:
    print("❌ Could not find TLP_YDAY in index.html")
    exit(1)
all_keys = list(json.loads(m.group(1)).keys())
print(f"  TLP keys in index.html: {len(all_keys)}")

def r2(v): return round(float(v), 2)
def awh(hrs, riders): return r2(hrs / riders) if riders > 0 else 0.0

TLP_YDAY           = {k: r2(yday_idx.get(k,{"hrs":0})["hrs"])                     for k in all_keys}
TLP_W7             = {k: r2(w7_idx.get(k,{"hrs":0})["hrs"] / W7_DAYS)             for k in all_keys}
TLP_MTD            = {k: r2(mtd_idx.get(k,{"hrs":0})["hrs"] / MTD_DAYS)           for k in all_keys}
TLP_MONTH          = {k: r2(lm_idx.get(k,{"hrs":0})["hrs"] / LM_DAYS)            for k in all_keys}
TLP_RIDERS_YDAY    = {k: int(yday_idx.get(k,{"riders":0})["riders"])              for k in all_keys}
TLP_RIDERS_MTD_SUM = {k: int(mtd_idx.get(k,{"riders":0})["riders"])              for k in all_keys}

def _awh(idx, k):
    d = idx.get(k,{"hrs":0,"riders":0})
    return awh(d["hrs"], d["riders"])

TLP_AWH_YDAY  = {k: _awh(yday_idx, k)                                              for k in all_keys}
TLP_AWH_W7    = {k: awh(w7_idx.get(k,{"hrs":0,"riders":0})["hrs"]/W7_DAYS,
                        w7_idx.get(k,{"hrs":0,"riders":0})["riders"]/W7_DAYS)     for k in all_keys}
TLP_AWH_MTD   = {k: awh(mtd_idx.get(k,{"hrs":0,"riders":0})["hrs"]/MTD_DAYS,
                        mtd_idx.get(k,{"hrs":0,"riders":0})["riders"]/MTD_DAYS)   for k in all_keys}
TLP_AWH_MONTH = {k: awh(lm_idx.get(k,{"hrs":0,"riders":0})["hrs"]/LM_DAYS,
                        lm_idx.get(k,{"hrs":0,"riders":0})["riders"]/LM_DAYS)     for k in all_keys}

# Spot check
ebad_key = "Nasr city|Ebad El rahman"
print(f"\nSpot-check {ebad_key}:")
print(f"  YDAY hrs    = {TLP_YDAY.get(ebad_key)} (W7/7 proxy)")
print(f"  W7 daily    = {TLP_W7.get(ebad_key)}")
print(f"  MTD daily   = {TLP_MTD.get(ebad_key)}")
print(f"  MONTH daily = {TLP_MONTH.get(ebad_key)}")

def patch_const(html, name, value):
    val = json.dumps(value, ensure_ascii=False)
    new, n = re.subn(rf'const {name} = \{{.*?\}};', f'const {name} = {val};', html, flags=re.DOTALL)
    print(f"  {name}: {n} sub(s)")
    return new

print("\nPatching 3PL constants:")
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

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(html)
print(f"✅ Patched index.html ({len(html):,} bytes)")
