import json
from datetime import date

today = date(2026, 9, 15)
yday  = date(2026, 9, 14)
week_start = date(2026, 9, 14)
MTD_DAYS = 14
LM_DAYS  = 31
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def r2(v): return round(float(v), 2)
def r4(v): return round(float(v), 4)

# ── Tableau zone data ──────────────────────────────────────────────────────────
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

# ── Looker shift data ──────────────────────────────────────────────────────────
shift_yday = {
    "Nasr city":  {"plannedHrs":16782.08,"lateLogin":0.0389,"breakMin":59.52,"acceptRate":0.8583},
    "Heliopolis": {"plannedHrs":15547.26,"lateLogin":0.0472,"breakMin":49.63,"acceptRate":0.8454},
    "Ain shams":  {"plannedHrs":2884.84, "lateLogin":0.0333,"breakMin":33.85,"acceptRate":0.8397},
}
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
ns_mtd = {
    "Nasr city":  {"noShow":0.0304,"riders":2726},
    "Heliopolis": {"noShow":0.0547,"riders":2803},
    "Ain shams":  {"noShow":0.0439,"riders":602},
}
shift_wtd = shift_yday; ns_wtd = ns_yday

sheet_rr = {
    "yday": {"Nasr city":0.9504,"Heliopolis":0.8666,"Ain shams":0.8833},
    "wtd":  {"Nasr city":0.995, "Heliopolis":0.961, "Ain shams":0.921},
    "mtd":  {"Nasr city":0.995, "Heliopolis":0.9611,"Ain shams":0.9206},
}

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

def zone_obj(tab, shift, ns, rr=None):
    sumHrs = tab['sumHrs']; orders = tab['orders']; riders = ns['riders']
    fill = shift['acceptRate']
    obj = {
        "riders":riders,"orders":orders,"sumHrs":r2(sumHrs),
        "plannedHrs":r2(shift['plannedHrs']),"lateLogin":r4(shift['lateLogin']),
        "noShow":r4(ns['noShow']),"breakMin":r2(shift['breakMin']),
        "fill":r4(fill),"acceptRate":r4(fill),"delivTime":r4(tab['delivTime']),
        "rat":r4(tab['rat']),"toVendor":r4(tab['toVendor']),
        "onTime":r4(tab['onTime']),"failRate":r4(tab['failRate']),
    }
    if rr is not None: obj['rr'] = rr
    return obj

# ── Offenders (from Looker browser export) ────────────────────────────────────
_off_rows = """H|2594862|21|5|6.7|16.2|31
H|4202995|11|0|0|0|11
H|2366868|11|2|0.6|28.7|15
H|2113059|11|0|0|0|11
H|4840081|10|0|0|0|10
H|4746818|10|9|15.2|19.6|23
H|4549182|10|4|11|14.1|14
H|4873078|10|1|0.6|8|11
H|4855750|10|6|9.4|33.7|23
H|4773174|9|15|16.8|40.2|31
H|1929761|9|3|2.7|19.3|12
H|1463655|9|1|5.2|17.7|13
H|2254017|8|0|10|13.1|10
H|2495115|7|1|10|24.9|11
H|4872726|7|0|0|0|7
H|2402774|7|0|2.5|8|8
H|1719311|7|0|3.5|16.5|9
H|1627104|7|2|13|16.2|10
H|3884095|7|0|3.8|34.7|15
H|4542744|7|2|9.1|30.7|11
H|1851271|7|2|5.4|15.9|11
H|2814310|7|0|0|0|7
H|4574579|7|0|2|14.2|9
H|1352533|7|0|0.7|11.6|8
H|3503957|7|3|17.7|31.3|18
H|4839915|7|0|0|0|7
H|2146457|6|0|0|0|6
H|4573472|6|3|18.9|19.4|13
H|4788262|6|0|24|30.2|15
H|4880494|6|6|2.2|48.2|15
H|4143943|6|0|3.7|62.8|17
H|4012626|6|0|15|34.7|12
H|4807994|6|6|9.4|26.5|13
H|4406017|6|8|6|54.9|15
H|2639837|6|0|0.7|40|11
H|2274346|6|17|14.6|60.6|27
H|1835046|6|6|0.5|89.7|12
H|4147649|6|14|49.2|42|38
H|4872859|6|0|2.6|54.9|13
H|4862144|6|0|0|0|6
H|4409100|6|3|12.6|28|13
H|2521462|6|3|1|37|13
H|2516497|6|2|9.7|51.1|15
H|4867806|6|0|0|0|6
H|4764413|6|1|1.2|69.9|15
H|4867865|6|5|4.8|32.6|12
H|2057424|6|1|2|1.8|7
H|4872771|5|10|12.9|46.6|20
H|4047348|5|0|0|31.6|7
H|4309974|5|0|25.1|38.8|16
H|2514528|5|3|29.8|41.3|16
H|1212774|5|1|18.9|11.2|8
H|4662777|5|2|23.9|42.2|11
H|4861412|5|1|0|0|6
H|4883827|5|0|0|0|5
H|4296556|5|0|0|0|5
H|1629686|5|6|7|57.3|14
H|1991116|5|1|9|32|15
H|4810797|5|1|1.7|31.8|11
H|4816518|5|0|0|0|5
H|2223894|5|0|11.3|26|8
H|4222761|5|0|4.5|61.6|14
H|2140297|5|0|0|18.2|7
H|4778255|5|3|8.5|24.2|12
H|4809245|5|4|13.1|26.6|13
H|4839654|5|6|7.7|37.2|11
H|1785355|5|3|17.5|31.8|13
H|4859041|5|5|1.5|70.7|15
H|2108245|5|11|37.1|28.7|19
H|4242766|5|0|10.3|26.2|13
H|4858500|5|0|13.7|38.7|14
H|1003577|5|0|7.3|10|7
H|4802521|5|11|25.3|40.8|22
H|4611590|5|1|3.1|41.5|8
H|1161000|5|0|1.1|16.4|7
H|3993839|5|3|14.3|26.4|10
H|2149988|5|0|3.5|50.7|10
H|4813650|5|4|4.5|37.7|9
H|4015605|5|7|4.2|62.8|15
H|4877535|5|4|5.8|39.3|10
H|4841610|5|0|0|0|5
H|4434457|4|0|0|47.9|11
H|4426337|4|0|11.5|21.6|6
H|4352210|4|0|11.9|52.6|13
H|4889522|4|0|0|0|4
H|4802382|4|1|8.6|69.3|15
H|4867861|4|5|2.2|80|10
H|2149052|4|0|1.1|62.3|8
H|4150674|4|0|15.3|22.7|7
H|3850343|4|3|1.5|26.9|9
H|2193371|4|4|2|53.4|10
H|2073274|4|0|0|0|4
H|2599467|4|2|6.8|70.9|23
H|4780432|4|5|4.4|66.7|10
H|2222699|4|0|3|20.8|5
H|907631|4|2|10.1|74.3|26
H|4523344|4|0|0|0|4
H|4679188|4|0|17.2|47.2|11
H|4710274|4|0|0|0|4
H|1597490|4|3|16.6|34.3|12
H|4891517|4|0|0|0|4
H|1950184|4|1|6.5|63.3|12
H|4171396|4|4|9.1|21.7|10
H|4877405|4|0|0|0|4
H|1301845|4|0|11.8|39.9|10
H|4494564|4|0|15.8|70.7|21
H|2521425|4|0|11.4|60.2|13
H|4801982|4|1|2.7|0.1|5
H|4872960|4|6|4.9|60.5|13
H|2092526|4|0|9.7|32.2|9
H|4776992|4|1|16.6|68.6|25
H|1756964|4|0|6.7|36|9
H|4859189|4|5|9.3|51.6|22
H|1881972|4|0|8|65.3|13
H|4810529|4|1|19.3|31.2|8
H|2430344|4|0|6.8|32.2|8
N|4387874|10|2|5.8|5.4|12
N|4874024|10|0|2.5|25.3|12
N|4873007|10|0|3.7|24.1|15
N|4707745|9|5|6|29.8|15
N|2654871|9|4|12|19.3|15
N|4715947|8|6|10.9|34.5|16
N|4813857|8|2|22.2|18.5|16
N|4862048|8|8|9.5|51.6|33
N|4056065|8|0|4.8|21.9|13
N|4810419|7|4|4.7|37|12
N|4310861|7|0|9.9|32.1|17
N|4877466|7|3|1.4|13.8|10
N|4739108|6|6|11|51.2|14
N|4871588|6|0|0|0|6
N|4884039|6|2|11.3|21.6|17
N|2077205|6|0|5.7|2.3|8
N|2100098|6|11|18.8|40.5|21
N|4877129|6|0|0|0|6
N|2024855|6|2|8.9|10.3|14
N|2502574|6|0|5.8|23.2|13
N|4842879|6|7|8.7|55.1|26
N|4877173|6|0|16.1|46.5|13
N|4858213|6|0|0|0|6
N|3996372|6|0|8.8|25.3|10
N|4848295|6|0|0|0|6
N|1653982|6|0|0|0|6
N|4464176|5|1|0.8|14.8|6
N|4877043|5|6|16.8|46.2|17
N|4846024|5|8|18|58.7|19
N|4845911|5|5|8.8|49.9|19
N|4848783|5|7|5.4|48.9|13
N|4873182|5|1|5.3|21.3|7
N|3674158|5|0|11.4|18|10
N|1336598|5|2|7.3|47.4|17
N|4841660|5|5|20.2|48.4|15
N|2160437|5|0|17.4|43.8|17
N|4877599|5|1|22.7|20.5|12
N|4752275|5|6|21.4|51.1|21
N|2023378|5|2|17.5|23.4|13
N|2050583|5|3|33.7|27.2|15
N|4883969|5|0|0|0|5
N|4724926|5|3|13.6|54.6|19
N|4691849|5|1|15|26.8|9
N|1432589|5|0|0|0|5
N|4633827|5|0|3.7|48.9|13
N|4825161|5|1|2|2.4|6
N|1581933|4|0|0.5|42.2|21
N|691762|4|2|11.7|38.5|14
N|4841334|4|3|19|32.8|9
N|3499066|4|3|9.5|37.9|11
N|4687272|4|9|20.7|47.2|22
N|4864196|4|1|3.7|25.8|6
N|4616204|4|5|9.1|42|9
N|2070739|4|0|4.5|60.5|12
N|3991358|4|1|6.3|9.9|6
N|3928148|4|0|5.1|54.8|10
N|4857443|4|0|0|0|4
N|3832699|4|0|1.5|44|8
N|1496335|4|10|4|48.2|14
N|4295081|4|0|0.3|79.3|15
N|4848398|4|12|34.4|25.4|18
A|4754806|10|0|0|0|10
A|2654773|8|0|8.5|22.3|15
A|4746793|7|11|15.4|45|27
A|4642949|7|3|2.8|39|10
A|4809254|6|0|0|0|6
A|4046863|6|8|19.7|40.2|20
A|4587875|5|0|1.8|55|12
A|4841685|5|0|0.1|54.2|12
A|4821109|5|0|0|0|5
A|4874076|5|4|16.8|49.3|15
A|4602572|5|0|6.3|62.6|15
A|4322266|5|7|24|54.1|25
A|4302649|5|4|0.1|48.3|13
A|4884268|5|2|4.9|31|9
A|4775540|5|0|0|0|5
A|4280168|5|1|2.6|46.1|9
A|4836366|4|0|0|0|4
A|4783262|4|8|13.3|67.8|17
A|3436768|4|2|6.2|33.7|10
A|4872950|4|2|10.3|68.4|21
A|4765585|4|0|0|0|4
A|1951560|4|6|17.1|27.5|15
A|1417543|4|1|0.2|80.4|29"""

_zmap = {'H':'Heliopolis','N':'Nasr city','A':'Ain shams'}
offenders = {"Nasr city":[],"Heliopolis":[],"Ain shams":[]}
for line in _off_rows.strip().split('\n'):
    p = line.split('|')
    zone = _zmap[p[0]]
    offenders[zone].append({"id":int(p[1]),"noShow":int(p[2]),"late":int(p[3]),"breaks":float(p[4]),"avp":float(p[5]),"shifts":int(p[6])})

print(f"Offenders: NC={len(offenders['Nasr city'])}, H={len(offenders['Heliopolis'])}, AS={len(offenders['Ain shams'])}")

# ── Hybrid SPs (E1 aggregated from browser) ───────────────────────────────────
hybrid_raw = {
    "yday": {
        "10186":{"riders":54,"actHrs":596.43,"planHrs":664.28,"noShow":0.0563,"lateLogin":0.1017},
        "10196":{"riders":77,"actHrs":913.19,"planHrs":974.52,"noShow":0.0439,"lateLogin":0.0233},
        "10198":{"riders":70,"actHrs":820.33,"planHrs":884.05,"noShow":0.0515,"lateLogin":0.0267},
        "10216":{"riders":44,"actHrs":510.38,"planHrs":511.42,"noShow":0.0,"lateLogin":0.0909},
        "10218":{"riders":83,"actHrs":995.22,"planHrs":1047.49,"noShow":0.0168,"lateLogin":0.0824},
        "10219":{"riders":75,"actHrs":738.65,"planHrs":766.56,"noShow":0.0917,"lateLogin":0.0097},
        "10229":{"riders":26,"actHrs":298.43,"planHrs":380.21,"noShow":0.1944,"lateLogin":0.0},
        "10230":{"riders":32,"actHrs":359.28,"planHrs":439.16,"noShow":0.1304,"lateLogin":0.0},
    },
    "mtd": {
        "10186":{"riders":65,"actHrs":6724.22,"planHrs":7127.3,"noShow":0.0317,"lateLogin":0.0534},
        "10196":{"riders":99,"actHrs":11050.36,"planHrs":11513.91,"noShow":0.0211,"lateLogin":0.0463},
        "10198":{"riders":84,"actHrs":10206.44,"planHrs":10510.99,"noShow":0.0043,"lateLogin":0.0334},
        "10216":{"riders":52,"actHrs":5888.15,"planHrs":6226.84,"noShow":0.0289,"lateLogin":0.0232},
        "10218":{"riders":90,"actHrs":10701.92,"planHrs":11243.43,"noShow":0.0103,"lateLogin":0.0928},
        "10219":{"riders":89,"actHrs":7754.77,"planHrs":8375.23,"noShow":0.0211,"lateLogin":0.0327},
        "10229":{"riders":36,"actHrs":3184.5,"planHrs":3841.63,"noShow":0.0818,"lateLogin":0.1554},
        "10230":{"riders":37,"actHrs":3780.88,"planHrs":4162.62,"noShow":0.0318,"lateLogin":0.0837},
    }
}

# Load existing for carry-forward (E2 order metrics timed out)
with open('/tmp/ncops/dashboard_data.json') as f:
    existing = json.load(f)

def merge_hybrid(new_e1, existing_period):
    out = {}
    for sp, vals in new_e1.items():
        ex = existing_period.get(sp, {})
        out[sp] = {**vals,
            "orders":ex.get('orders',0),"dt":ex.get('dt',0),
            "rat":ex.get('rat',0),"tv":ex.get('tv',0),
            "tc":ex.get('tc',0),"onTime":ex.get('onTime',0),"breakMin":ex.get('breakMin',0),
        }
    return out

hybrid_yday = merge_hybrid(hybrid_raw['yday'], existing['hybrid']['yday'])
hybrid_wtd  = merge_hybrid(hybrid_raw['yday'], existing['hybrid']['wtd'])
hybrid_mtd  = merge_hybrid(hybrid_raw['mtd'],  existing['hybrid']['mtd'])

# ── Tmart perf (Section F) ─────────────────────────────────────────────────────
# All vendors had 0 orders in the query date range; tv values captured
_perf_tv = {
    "619844":{"pyd":2.35,"pl3":2.11,"pl7":1.98,"pmtd":2.04,"plm":2.11},
    "619849":{"pyd":2.43,"pl3":2.04,"pl7":2.2, "pmtd":2.33,"plm":1.94},
    "620008":{"pyd":1.11,"pl3":1.31,"pl7":1.03,"pmtd":1.17,"plm":1.09},
    "655461":{"pyd":2.09,"pl3":2.94,"pl7":2.7, "pmtd":2.74,"plm":2.65},
    "717765":{"pyd":2.16,"pl3":2.34,"pl7":2.59,"pmtd":2.7, "plm":1.65},
    "760059":{"pyd":1.97,"pl3":1.86,"pl7":1.75,"pmtd":1.91,"plm":1.79},
    "783048":{"pyd":0.84,"pl3":1.08,"pl7":0.93,"pmtd":0.95,"plm":0.95},
    "793636":{"pyd":1.19,"pl3":1.47,"pl7":1.22,"pmtd":1.4, "plm":1.47},
    "801850":{"pyd":3.0, "pl3":2.97,"pl7":2.86,"pmtd":3.14,"plm":2.74},
}
def make_perf(period_key):
    out = {}
    for vc, tv_vals in _perf_tv.items():
        out[vc] = {"orders_total":0,"dt":0,"rat":0,"tv":tv_vals[period_key],
                   "tc":0,"avtc":0,"l10":0,"l5":0,"ot":0,"fir":0}
    return out

perf_yday = make_perf("pyd")
perf_l3d  = make_perf("pl3")
perf_l7d  = make_perf("pl7")
perf_mtd  = make_perf("pmtd")
perf_lm   = make_perf("plm")
perf_l14d = existing['perf'].get('l14d', {})
perf_shift = existing.get('perf_shift', {})

# ── 3PL TLP (pre-aggregated from browser) ────────────────────────────────────
# Format: "Zone|Contract": {yday, w7, mtd, month, riders_yday, riders_mtd_sum, awh_yday, awh_w7, awh_mtd, awh_month}
_tlp_raw = {
"Heliopolis|Al Alamia":{"yday":1320.03,"w7":1155.98,"mtd":1240.1,"month":1383.49,"riders_yday":154,"riders_mtd_sum":2085,"awh_yday":8.57,"awh_w7":8.49,"awh_mtd":116.58,"awh_month":254.85},
"Ain shams|Al Alamia":{"yday":475.69,"w7":417.29,"mtd":487.09,"month":561.4,"riders_yday":66,"riders_mtd_sum":898,"awh_yday":7.21,"awh_w7":7.32,"awh_mtd":106.31,"awh_month":247.03},
"Nasr city|Al Alamia":{"yday":890.05,"w7":710.13,"mtd":742.0,"month":817.89,"riders_yday":95,"riders_mtd_sum":1095,"awh_yday":9.37,"awh_w7":9.73,"awh_mtd":132.81,"awh_month":298.06},
"Heliopolis|Apache":{"yday":158.33,"w7":179.15,"mtd":206.67,"month":202.69,"riders_yday":24,"riders_mtd_sum":402,"awh_yday":6.6,"awh_w7":7.33,"awh_mtd":100.76,"awh_month":214.76},
"Ain shams|Apache":{"yday":126.09,"w7":104.46,"mtd":108.31,"month":102.99,"riders_yday":18,"riders_mtd_sum":247,"awh_yday":7.01,"awh_w7":6.09,"awh_mtd":85.94,"awh_month":183.96},
"Nasr city|Apache":{"yday":195.66,"w7":173.23,"mtd":204.41,"month":177.27,"riders_yday":28,"riders_mtd_sum":388,"awh_yday":6.99,"awh_w7":7.01,"awh_mtd":103.26,"awh_month":226.85},
"Nasr city|Barg":{"yday":231.15,"w7":249.68,"mtd":284.62,"month":341.0,"riders_yday":33,"riders_mtd_sum":476,"awh_yday":7.0,"awh_w7":8.28,"awh_mtd":117.2,"awh_month":274.0},
"Heliopolis|Barg":{"yday":455.92,"w7":406.62,"mtd":404.34,"month":481.92,"riders_yday":56,"riders_mtd_sum":713,"awh_yday":8.14,"awh_w7":8.52,"awh_mtd":111.15,"awh_month":246.47},
"Ain shams|Barg":{"yday":52.28,"w7":47.36,"mtd":57.71,"month":71.53,"riders_yday":8,"riders_mtd_sum":117,"awh_yday":6.53,"awh_w7":6.37,"awh_mtd":96.67,"awh_month":234.59},
"Nasr city|BeCool":{"yday":95.79,"w7":81.3,"mtd":88.22,"month":96.94,"riders_yday":14,"riders_mtd_sum":191,"awh_yday":6.84,"awh_w7":6.54,"awh_mtd":90.53,"awh_month":205.19},
"Heliopolis|BeCool":{"yday":186.12,"w7":132.89,"mtd":137.76,"month":138.9,"riders_yday":23,"riders_mtd_sum":272,"awh_yday":8.09,"awh_w7":7.38,"awh_mtd":99.27,"awh_month":211.55},
"Nasr city|Bedaya":{"yday":117.97,"w7":128.48,"mtd":124.37,"month":119.05,"riders_yday":14,"riders_mtd_sum":178,"awh_yday":8.43,"awh_w7":9.57,"awh_mtd":136.95,"awh_month":272.4},
"Nasr city|Courier for delivery":{"yday":179.95,"w7":246.5,"mtd":259.7,"month":329.0,"riders_yday":26,"riders_mtd_sum":458,"awh_yday":6.92,"awh_w7":8.14,"awh_mtd":111.14,"awh_month":246.05},
"Heliopolis|Courier for delivery":{"yday":200.35,"w7":169.94,"mtd":185.09,"month":235.05,"riders_yday":32,"riders_mtd_sum":403,"awh_yday":6.26,"awh_w7":6.4,"awh_mtd":90.02,"awh_month":212.3},
"Nasr city|Ebad El rahman":{"yday":3391.85,"w7":2990.0,"mtd":3218.61,"month":3748.92,"riders_yday":391,"riders_mtd_sum":5153,"awh_yday":8.67,"awh_w7":8.9,"awh_mtd":122.42,"awh_month":265.24},
"Heliopolis|Ebad El rahman":{"yday":3081.92,"w7":2562.56,"mtd":2671.52,"month":2877.58,"riders_yday":382,"riders_mtd_sum":4706,"awh_yday":8.07,"awh_w7":8.13,"awh_mtd":111.27,"awh_month":246.33},
"Nasr city|El Abtal":{"yday":1855.75,"w7":1496.33,"mtd":1664.7,"month":1811.43,"riders_yday":199,"riders_mtd_sum":2529,"awh_yday":9.33,"awh_w7":9.29,"awh_mtd":129.02,"awh_month":286.88},
"Heliopolis|El Abtal":{"yday":602.56,"w7":615.05,"mtd":678.81,"month":725.34,"riders_yday":87,"riders_mtd_sum":1267,"awh_yday":6.93,"awh_w7":7.42,"awh_mtd":105.01,"awh_month":228.92},
"Nasr city|El Ezz":{"yday":439.09,"w7":413.2,"mtd":435.19,"month":446.2,"riders_yday":52,"riders_mtd_sum":720,"awh_yday":8.44,"awh_w7":8.53,"awh_mtd":118.47,"awh_month":270.71},
"Heliopolis|El Ezz":{"yday":578.57,"w7":569.89,"mtd":615.77,"month":645.92,"riders_yday":79,"riders_mtd_sum":1137,"awh_yday":7.32,"awh_w7":7.72,"awh_mtd":106.15,"awh_month":237.92},
"Nasr city|El Tohami":{"yday":595.54,"w7":546.39,"mtd":592.17,"month":581.82,"riders_yday":71,"riders_mtd_sum":905,"awh_yday":8.39,"awh_w7":9.13,"awh_mtd":128.25,"awh_month":276.66},
"Heliopolis|El Tohami":{"yday":485.48,"w7":347.9,"mtd":377.14,"month":431.84,"riders_yday":62,"riders_mtd_sum":726,"awh_yday":7.83,"awh_w7":7.38,"awh_mtd":101.82,"awh_month":228.78},
"Ain shams|El Tohami":{"yday":52.52,"w7":58.98,"mtd":69.31,"month":77.4,"riders_yday":9,"riders_mtd_sum":150,"awh_yday":5.84,"awh_w7":6.07,"awh_mtd":90.56,"awh_month":187.83},
"Heliopolis|Full Speed":{"yday":677.63,"w7":558.68,"mtd":600.98,"month":657.14,"riders_yday":85,"riders_mtd_sum":1097,"awh_yday":7.97,"awh_w7":7.74,"awh_mtd":107.38,"awh_month":244.96},
"Nasr city|Full Speed":{"yday":317.96,"w7":252.42,"mtd":285.7,"month":350.55,"riders_yday":36,"riders_mtd_sum":490,"awh_yday":8.83,"awh_w7":7.75,"awh_mtd":114.28,"awh_month":272.56},
"Ain shams|Full Speed":{"yday":55.47,"w7":64.95,"mtd":70.85,"month":66.38,"riders_yday":14,"riders_mtd_sum":173,"awh_yday":3.96,"awh_w7":5.75,"awh_mtd":80.27,"awh_month":187.06},
"Nasr city|Glesco":{"yday":71.82,"w7":39.05,"mtd":41.93,"month":21.5,"riders_yday":9,"riders_mtd_sum":73,"awh_yday":7.98,"awh_w7":7.81,"awh_mtd":112.57,"awh_month":237.5},
"Nasr city|Jasson":{"yday":334.12,"w7":315.82,"mtd":314.04,"month":340.18,"riders_yday":36,"riders_mtd_sum":500,"awh_yday":9.28,"awh_w7":9.1,"awh_mtd":123.1,"awh_month":280.85},
"Ain shams|Jasson":{"yday":223.86,"w7":160.98,"mtd":188.93,"month":176.91,"riders_yday":35,"riders_mtd_sum":386,"awh_yday":6.4,"awh_w7":6.63,"awh_mtd":95.94,"awh_month":200.48},
"Heliopolis|Jasson":{"yday":631.97,"w7":555.84,"mtd":619.97,"month":683.06,"riders_yday":75,"riders_mtd_sum":1019,"awh_yday":8.43,"awh_w7":8.55,"awh_mtd":119.25,"awh_month":246.4},
"Nasr city|MR Delivery":{"yday":162.46,"w7":160.43,"mtd":176.16,"month":177.26,"riders_yday":26,"riders_mtd_sum":332,"awh_yday":6.25,"awh_w7":7.49,"awh_mtd":104.0,"awh_month":215.63},
"Ain shams|MR Delivery":{"yday":24.42,"w7":20.24,"mtd":26.24,"month":34.78,"riders_yday":4,"riders_mtd_sum":46,"awh_yday":6.1,"awh_w7":9.45,"awh_mtd":111.8,"awh_month":240.45},
"Heliopolis|MTA":{"yday":733.86,"w7":590.27,"mtd":607.58,"month":663.77,"riders_yday":91,"riders_mtd_sum":1137,"awh_yday":8.06,"awh_w7":7.54,"awh_mtd":104.74,"awh_month":231.37},
"Ain shams|MTA":{"yday":267.95,"w7":236.82,"mtd":243.44,"month":246.18,"riders_yday":28,"riders_mtd_sum":418,"awh_yday":9.57,"awh_w7":8.42,"awh_mtd":114.15,"awh_month":237.53},
"Nasr city|MTA":{"yday":278.14,"w7":275.84,"mtd":298.65,"month":335.62,"riders_yday":34,"riders_mtd_sum":499,"awh_yday":8.18,"awh_w7":8.29,"awh_mtd":117.31,"awh_month":246.58},
"Heliopolis|Noot":{"yday":110.95,"w7":128.17,"mtd":142.44,"month":167.6,"riders_yday":15,"riders_mtd_sum":254,"awh_yday":7.4,"awh_w7":8.08,"awh_mtd":109.91,"awh_month":251.66},
"Heliopolis|Speedo":{"yday":712.92,"w7":666.3,"mtd":718.82,"month":801.96,"riders_yday":91,"riders_mtd_sum":1370,"awh_yday":7.83,"awh_w7":7.5,"awh_mtd":102.84,"awh_month":227.54},
"Nasr city|Speedo":{"yday":920.91,"w7":917.86,"mtd":982.74,"month":1051.69,"riders_yday":108,"riders_mtd_sum":1587,"awh_yday":8.53,"awh_w7":8.84,"awh_mtd":121.37,"awh_month":257.63},
"Ain shams|Speedo":{"yday":118.89,"w7":93.08,"mtd":98.58,"month":85.71,"riders_yday":19,"riders_mtd_sum":221,"awh_yday":6.26,"awh_w7":6.09,"awh_mtd":87.43,"awh_month":188.92},
"Nasr city|Stop Car":{"yday":928.06,"w7":833.18,"mtd":885.89,"month":1032.48,"riders_yday":113,"riders_mtd_sum":1460,"awh_yday":8.21,"awh_w7":8.69,"awh_mtd":118.93,"awh_month":257.05},
"Heliopolis|Stop Car":{"yday":236.57,"w7":166.25,"mtd":198.64,"month":197.09,"riders_yday":28,"riders_mtd_sum":347,"awh_yday":8.45,"awh_w7":8.14,"awh_mtd":112.2,"awh_month":253.89},
"Ain shams|Stop Car":{"yday":297.89,"w7":229.73,"mtd":242.78,"month":265.28,"riders_yday":34,"riders_mtd_sum":392,"awh_yday":8.76,"awh_w7":8.6,"awh_mtd":121.39,"awh_month":245.6},
"Nasr city|Super Speed":{"yday":374.58,"w7":353.37,"mtd":409.25,"month":416.84,"riders_yday":45,"riders_mtd_sum":666,"awh_yday":8.32,"awh_w7":8.53,"awh_mtd":120.44,"awh_month":255.15},
"Heliopolis|Super Speed":{"yday":204.12,"w7":174.08,"mtd":189.19,"month":197.06,"riders_yday":26,"riders_mtd_sum":353,"awh_yday":7.85,"awh_w7":7.48,"awh_mtd":105.04,"awh_month":235.55},
"Heliopolis|Tanta Car":{"yday":117.95,"w7":139.15,"mtd":149.59,"month":174.1,"riders_yday":18,"riders_mtd_sum":311,"awh_yday":6.55,"awh_w7":6.76,"awh_mtd":94.27,"awh_month":205.55},
"Ain shams|Tanta Car":{"yday":73.34,"w7":106.28,"mtd":114.68,"month":88.49,"riders_yday":11,"riders_mtd_sum":220,"awh_yday":6.67,"awh_w7":7.09,"awh_mtd":102.17,"awh_month":223.19},
"Heliopolis|Team mh for Delivery":{"yday":1097.09,"w7":860.83,"mtd":907.2,"month":1034.42,"riders_yday":116,"riders_mtd_sum":1385,"awh_yday":9.46,"awh_w7":9.17,"awh_mtd":128.38,"awh_month":288.05},
"Nasr city|Team mh for Delivery":{"yday":1225.77,"w7":1082.21,"mtd":1159.05,"month":1210.63,"riders_yday":126,"riders_mtd_sum":1620,"awh_yday":9.73,"awh_w7":10.07,"awh_mtd":140.23,"awh_month":309.34},
"Heliopolis|Top delivery":{"yday":985.05,"w7":882.25,"mtd":1025.03,"month":1083.11,"riders_yday":118,"riders_mtd_sum":1663,"awh_yday":8.35,"awh_w7":8.51,"awh_mtd":120.81,"awh_month":254.31},
"Nasr city|Top delivery":{"yday":261.43,"w7":206.36,"mtd":242.97,"month":344.21,"riders_yday":36,"riders_mtd_sum":453,"awh_yday":7.26,"awh_w7":7.45,"awh_mtd":105.13,"awh_month":268.94},
"Heliopolis|Wakeel":{"yday":118.69,"w7":101.85,"mtd":107.19,"month":95.67,"riders_yday":13,"riders_mtd_sum":149,"awh_yday":9.13,"awh_w7":10.33,"awh_mtd":141.0,"awh_month":287.3},
"Nasr city|Wakeel":{"yday":63.75,"w7":47.43,"mtd":57.59,"month":46.05,"riders_yday":6,"riders_mtd_sum":105,"awh_yday":10.63,"awh_w7":7.91,"awh_mtd":107.51,"awh_month":231.69},
"Heliopolis|Zero Zero Seven":{"yday":12.38,"w7":7.32,"mtd":13.46,"month":9.38,"riders_yday":3,"riders_mtd_sum":22,"awh_yday":4.13,"awh_w7":8.54,"awh_mtd":119.88,"awh_month":173.32},
"Nasr city|Zero Zero Seven":{"yday":134.56,"w7":111.2,"mtd":132.61,"month":134.55,"riders_yday":18,"riders_mtd_sum":230,"awh_yday":7.48,"awh_w7":8.11,"awh_mtd":113.0,"awh_month":232.14},
"Heliopolis|el Dawlya":{"yday":23.23,"w7":17.49,"mtd":18.74,"month":19.39,"riders_yday":3,"riders_mtd_sum":32,"awh_yday":7.74,"awh_w7":8.16,"awh_mtd":114.79,"awh_month":235.88},
"Heliopolis|Bedaya":{"yday":26.54,"w7":16.07,"mtd":16.44,"month":23.87,"riders_yday":3,"riders_mtd_sum":34,"awh_yday":8.85,"awh_w7":7.03,"awh_mtd":94.76,"awh_month":241.46},
"Ain shams|Ebad El rahman":{"yday":145.02,"w7":106.24,"mtd":115.11,"month":136.88,"riders_yday":22,"riders_mtd_sum":268,"awh_yday":6.59,"awh_w7":5.95,"awh_mtd":84.19,"awh_month":194.59},
"Ain shams|El Ezz":{"yday":15.09,"w7":36.01,"mtd":46.62,"month":42.67,"riders_yday":4,"riders_mtd_sum":110,"awh_yday":3.77,"awh_w7":5.73,"awh_mtd":83.07,"awh_month":195.28},
"Heliopolis|MR Delivery":{"yday":180.27,"w7":185.85,"mtd":208.04,"month":233.51,"riders_yday":27,"riders_mtd_sum":451,"awh_yday":6.68,"awh_w7":6.28,"awh_mtd":90.41,"awh_month":207.59},
"Ain shams|Noot":{"yday":26.24,"w7":26.32,"mtd":29.41,"month":33.68,"riders_yday":3,"riders_mtd_sum":54,"awh_yday":8.75,"awh_w7":7.68,"awh_mtd":106.74,"awh_month":247.09},
"Nasr city|Noot":{"yday":112.82,"w7":101.31,"mtd":99.93,"month":149.34,"riders_yday":14,"riders_mtd_sum":169,"awh_yday":8.06,"awh_w7":8.75,"awh_mtd":115.89,"awh_month":252.23},
"Nasr city|SOG":{"yday":164.05,"w7":128.52,"mtd":144.33,"month":156.15,"riders_yday":17,"riders_mtd_sum":259,"awh_yday":9.65,"awh_w7":8.18,"awh_mtd":109.22,"awh_month":237.81},
"Heliopolis|Tanta":{"yday":31.76,"w7":42.66,"mtd":43.02,"month":49.61,"riders_yday":7,"riders_mtd_sum":81,"awh_yday":4.54,"awh_w7":7.86,"awh_mtd":104.11,"awh_month":206.39},
"Nasr city|Tanta":{"yday":364.75,"w7":304.38,"mtd":306.47,"month":466.21,"riders_yday":43,"riders_mtd_sum":456,"awh_yday":8.48,"awh_w7":9.68,"awh_mtd":131.73,"awh_month":304.99},
"Nasr city|Tanta Car":{"yday":377.89,"w7":277.77,"mtd":250.51,"month":266.62,"riders_yday":45,"riders_mtd_sum":437,"awh_yday":8.4,"awh_w7":8.38,"awh_mtd":112.36,"awh_month":263.88},
"Ain shams|Top delivery":{"yday":275.15,"w7":283.45,"mtd":276.16,"month":306.1,"riders_yday":36,"riders_mtd_sum":543,"awh_yday":7.64,"awh_w7":7.43,"awh_mtd":99.68,"awh_month":209.82},
"Ain shams|Team mh for Delivery":{"yday":25.96,"w7":46.94,"mtd":49.36,"month":58.97,"riders_yday":5,"riders_mtd_sum":122,"awh_yday":5.19,"awh_w7":6.32,"awh_mtd":79.3,"awh_month":177.65},
"Ain shams|Wakeel":{"yday":32.25,"w7":48.04,"mtd":49.8,"month":58.81,"riders_yday":7,"riders_mtd_sum":98,"awh_yday":4.61,"awh_w7":7.15,"awh_mtd":99.6,"awh_month":204.75},
"Ain shams|Courier for delivery":{"yday":46.89,"w7":44.19,"mtd":43.86,"month":40.28,"riders_yday":8,"riders_mtd_sum":104,"awh_yday":5.86,"awh_w7":5.84,"awh_mtd":82.67,"awh_month":189.74},
"Nasr city|Gearz":{"yday":0.0,"w7":0.0,"mtd":0.0,"month":0.12,"riders_yday":0,"riders_mtd_sum":0,"awh_yday":0.0,"awh_w7":0.0,"awh_mtd":0.0,"awh_month":115.9},
}

# Build TLP dicts for dashboard
TLP_YDAY={}; TLP_W7={}; TLP_MTD={}; TLP_MONTH={}
TLP_RIDERS_YDAY={}; TLP_RIDERS_MTD_SUM={}
TLP_AWH_YDAY={}; TLP_AWH_W7={}; TLP_AWH_MTD={}; TLP_AWH_MONTH={}
for k, v in _tlp_raw.items():
    TLP_YDAY[k]=v['yday']; TLP_W7[k]=v['w7']; TLP_MTD[k]=v['mtd']; TLP_MONTH[k]=v['month']
    TLP_RIDERS_YDAY[k]=v['riders_yday']; TLP_RIDERS_MTD_SUM[k]=v['riders_mtd_sum']
    TLP_AWH_YDAY[k]=v['awh_yday']; TLP_AWH_W7[k]=v['awh_w7']; TLP_AWH_MTD[k]=v['awh_mtd']; TLP_AWH_MONTH[k]=v['awh_month']

# ── Assemble final data ────────────────────────────────────────────────────────
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
    "tlp_riders_yday":    TLP_RIDERS_YDAY,
    "tlp_riders_mtd_sum": TLP_RIDERS_MTD_SUM,
    "tlp_awh_yday":  TLP_AWH_YDAY,
    "tlp_awh_w7":    TLP_AWH_W7,
    "tlp_awh_mtd":   TLP_AWH_MTD,
    "tlp_awh_month": TLP_AWH_MONTH,
}

with open('/tmp/ncops/dashboard_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✓ dashboard_data.json written")
print(f"  Zones: {list(data['zone']['yday'].keys())}")
print(f"  Offenders: NC={len(offenders['Nasr city'])}, H={len(offenders['Heliopolis'])}, AS={len(offenders['Ain shams'])}")
print(f"  Hybrid SPs: {sorted(hybrid_yday.keys())}")
print(f"  Perf vendors: {sorted(perf_yday.keys())}")
print(f"  TLP keys: {len(TLP_YDAY)}")
