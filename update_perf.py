import json

PERF_DATA = {
    "619844": {
        "lm":   {"orders_total":2816,"dt":17.7,"rat":1.3,"tv":3.6,"l10":0.05,"l5":0.18,"tc":2.9,"avtc":4.9,"ot":0.82,"fir":1.0},
        "mtd":  {"orders_total":2817,"dt":17.3,"rat":1.0,"tv":3.2,"l10":0.04,"l5":0.15,"tc":3.1,"avtc":4.9,"ot":0.85,"fir":1.0},
        "l14d": {"orders_total":2804,"dt":15.7,"rat":0.7,"tv":2.4,"l10":0.02,"l5":0.10,"tc":3.1,"avtc":4.5,"ot":0.90,"fir":1.0},
        "l7d":  {"orders_total":2838,"dt":15.5,"rat":0.7,"tv":2.3,"l10":0.02,"l5":0.09,"tc":3.0,"avtc":4.5,"ot":0.91,"fir":1.0},
        "l3d":  {"orders_total":2864,"dt":15.4,"rat":0.7,"tv":2.3,"l10":0.02,"l5":0.09,"tc":3.0,"avtc":4.5,"ot":0.91,"fir":1.0},
        "yday": {"orders_total":2972,"dt":16.2,"rat":0.8,"tv":2.5,"l10":0.02,"l5":0.09,"tc":3.1,"avtc":4.8,"ot":0.91,"fir":1.0},
    },
    "619849": {
        "lm":   {"orders_total":2060,"dt":15.0,"rat":1.0,"tv":2.8,"l10":0.03,"l5":0.14,"tc":2.7,"avtc":3.2,"ot":0.86,"fir":1.0},
        "mtd":  {"orders_total":2022,"dt":15.4,"rat":1.3,"tv":3.2,"l10":0.04,"l5":0.16,"tc":3.0,"avtc":3.3,"ot":0.84,"fir":1.0},
        "l14d": {"orders_total":2009,"dt":14.1,"rat":0.8,"tv":2.4,"l10":0.03,"l5":0.11,"tc":2.9,"avtc":3.2,"ot":0.89,"fir":1.0},
        "l7d":  {"orders_total":1988,"dt":13.9,"rat":0.8,"tv":2.1,"l10":0.02,"l5":0.10,"tc":2.9,"avtc":3.3,"ot":0.90,"fir":1.0},
        "l3d":  {"orders_total":1977,"dt":13.3,"rat":0.7,"tv":1.6,"l10":0.02,"l5":0.07,"tc":2.8,"avtc":3.2,"ot":0.93,"fir":1.0},
        "yday": {"orders_total":2091,"dt":13.4,"rat":0.6,"tv":1.5,"l10":0.02,"l5":0.06,"tc":2.8,"avtc":3.2,"ot":0.94,"fir":1.0},
    },
    "620008": {
        "lm":   {"orders_total":1474,"dt":13.5,"rat":0.8,"tv":2.2,"l10":0.02,"l5":0.09,"tc":2.5,"avtc":4.0,"ot":0.91,"fir":1.0},
        "mtd":  {"orders_total":1530,"dt":11.8,"rat":0.6,"tv":1.6,"l10":0.02,"l5":0.07,"tc":2.3,"avtc":3.3,"ot":0.93,"fir":1.0},
        "l14d": {"orders_total":1516,"dt":11.6,"rat":0.5,"tv":1.4,"l10":0.01,"l5":0.06,"tc":2.4,"avtc":3.4,"ot":0.94,"fir":1.0},
        "l7d":  {"orders_total":1519,"dt":11.7,"rat":0.4,"tv":1.4,"l10":0.01,"l5":0.06,"tc":2.6,"avtc":3.6,"ot":0.94,"fir":1.0},
        "l3d":  {"orders_total":1430,"dt":11.2,"rat":0.4,"tv":1.2,"l10":0.01,"l5":0.05,"tc":2.5,"avtc":3.4,"ot":0.95,"fir":1.0},
        "yday": {"orders_total":1748,"dt":11.5,"rat":0.5,"tv":1.6,"l10":0.01,"l5":0.05,"tc":2.7,"avtc":3.3,"ot":0.95,"fir":1.0},
    },
    "655461": {
        "lm":   {"orders_total":2293,"dt":21.9,"rat":2.3,"tv":4.7,"l10":0.07,"l5":0.21,"tc":3.4,"avtc":5.7,"ot":0.79,"fir":1.0},
        "mtd":  {"orders_total":2296,"dt":22.5,"rat":2.5,"tv":5.2,"l10":0.09,"l5":0.24,"tc":3.5,"avtc":5.9,"ot":0.76,"fir":1.0},
        "l14d": {"orders_total":2281,"dt":22.6,"rat":2.4,"tv":5.0,"l10":0.09,"l5":0.23,"tc":3.9,"avtc":6.2,"ot":0.77,"fir":1.0},
        "l7d":  {"orders_total":2328,"dt":23.9,"rat":2.6,"tv":5.2,"l10":0.09,"l5":0.24,"tc":5.0,"avtc":7.1,"ot":0.76,"fir":1.0},
        "l3d":  {"orders_total":2394,"dt":24.9,"rat":2.2,"tv":4.8,"l10":0.07,"l5":0.20,"tc":6.2,"avtc":8.3,"ot":0.80,"fir":1.0},
        "yday": {"orders_total":2321,"dt":26.8,"rat":2.4,"tv":5.1,"l10":0.08,"l5":0.20,"tc":6.9,"avtc":9.5,"ot":0.80,"fir":1.0},
    },
    "717765": {
        "lm":   {"orders_total":2596,"dt":18.5,"rat":1.2,"tv":3.0,"l10":0.04,"l5":0.11,"tc":4.5,"avtc":5.4,"ot":0.89,"fir":1.0},
        "mtd":  {"orders_total":2628,"dt":17.7,"rat":1.1,"tv":2.8,"l10":0.03,"l5":0.10,"tc":4.2,"avtc":4.7,"ot":0.90,"fir":1.0},
        "l14d": {"orders_total":2619,"dt":15.8,"rat":0.8,"tv":1.8,"l10":0.02,"l5":0.06,"tc":3.1,"avtc":4.1,"ot":0.94,"fir":1.0},
        "l7d":  {"orders_total":2701,"dt":15.7,"rat":0.8,"tv":1.6,"l10":0.02,"l5":0.06,"tc":3.3,"avtc":4.1,"ot":0.94,"fir":1.0},
        "l3d":  {"orders_total":2745,"dt":15.8,"rat":0.9,"tv":1.7,"l10":0.02,"l5":0.06,"tc":3.5,"avtc":4.2,"ot":0.94,"fir":1.0},
        "yday": {"orders_total":2830,"dt":16.8,"rat":1.0,"tv":1.8,"l10":0.02,"l5":0.06,"tc":4.1,"avtc":4.7,"ot":0.94,"fir":1.0},
    },
    "760059": {
        "lm":   {"orders_total":2019,"dt":16.2,"rat":1.0,"tv":2.9,"l10":0.03,"l5":0.12,"tc":2.9,"avtc":4.4,"ot":0.88,"fir":1.0},
        "mtd":  {"orders_total":1933,"dt":16.8,"rat":1.3,"tv":3.1,"l10":0.04,"l5":0.14,"tc":3.2,"avtc":5.0,"ot":0.86,"fir":1.0},
        "l14d": {"orders_total":1991,"dt":16.1,"rat":0.9,"tv":2.5,"l10":0.03,"l5":0.10,"tc":2.9,"avtc":5.0,"ot":0.90,"fir":1.0},
        "l7d":  {"orders_total":1936,"dt":16.2,"rat":0.9,"tv":2.5,"l10":0.03,"l5":0.10,"tc":2.9,"avtc":5.2,"ot":0.90,"fir":1.0},
        "l3d":  {"orders_total":1863,"dt":16.5,"rat":0.9,"tv":2.4,"l10":0.03,"l5":0.09,"tc":2.9,"avtc":5.4,"ot":0.91,"fir":1.0},
        "yday": {"orders_total":2171,"dt":16.4,"rat":0.7,"tv":2.0,"l10":0.02,"l5":0.07,"tc":3.2,"avtc":5.7,"ot":0.93,"fir":1.0},
    },
    "783048": {
        "lm":   {"orders_total":2306,"dt":12.8,"rat":0.9,"tv":2.3,"l10":0.02,"l5":0.09,"tc":2.3,"avtc":3.5,"ot":0.91,"fir":1.0},
        "mtd":  {"orders_total":2424,"dt":11.5,"rat":0.6,"tv":1.6,"l10":0.02,"l5":0.07,"tc":2.5,"avtc":3.2,"ot":0.93,"fir":1.0},
        "l14d": {"orders_total":2407,"dt":11.0,"rat":0.4,"tv":1.2,"l10":0.01,"l5":0.05,"tc":2.6,"avtc":3.2,"ot":0.95,"fir":1.0},
        "l7d":  {"orders_total":2409,"dt":10.8,"rat":0.4,"tv":1.0,"l10":0.01,"l5":0.04,"tc":2.6,"avtc":3.2,"ot":0.96,"fir":1.0},
        "l3d":  {"orders_total":2379,"dt":10.5,"rat":0.4,"tv":1.0,"l10":0.01,"l5":0.04,"tc":2.5,"avtc":3.1,"ot":0.96,"fir":1.0},
        "yday": {"orders_total":2529,"dt":11.0,"rat":0.5,"tv":1.2,"l10":0.02,"l5":0.05,"tc":2.6,"avtc":3.2,"ot":0.95,"fir":1.0},
    },
    "793636": {
        "lm":   {"orders_total":2141,"dt":13.2,"rat":0.9,"tv":2.6,"l10":0.03,"l5":0.12,"tc":2.2,"avtc":3.4,"ot":0.88,"fir":1.0},
        "mtd":  {"orders_total":2205,"dt":12.8,"rat":0.9,"tv":2.3,"l10":0.03,"l5":0.11,"tc":2.5,"avtc":3.5,"ot":0.89,"fir":1.0},
        "l14d": {"orders_total":2209,"dt":11.7,"rat":0.6,"tv":1.7,"l10":0.02,"l5":0.07,"tc":2.5,"avtc":3.4,"ot":0.93,"fir":1.0},
        "l7d":  {"orders_total":2227,"dt":11.6,"rat":0.6,"tv":1.5,"l10":0.02,"l5":0.06,"tc":2.6,"avtc":3.5,"ot":0.94,"fir":1.0},
        "l3d":  {"orders_total":2225,"dt":11.6,"rat":0.6,"tv":1.7,"l10":0.02,"l5":0.07,"tc":2.4,"avtc":3.4,"ot":0.93,"fir":1.0},
        "yday": {"orders_total":2327,"dt":12.2,"rat":0.7,"tv":1.9,"l10":0.02,"l5":0.08,"tc":2.5,"avtc":3.5,"ot":0.92,"fir":1.0},
    },
    "801850": {
        "lm":   {"orders_total":1148,"dt":16.4,"rat":1.0,"tv":3.7,"l10":0.05,"l5":0.19,"tc":2.2,"avtc":5.0,"ot":0.81,"fir":1.0},
        "mtd":  {"orders_total":1199,"dt":16.7,"rat":1.3,"tv":4.1,"l10":0.06,"l5":0.22,"tc":2.2,"avtc":5.0,"ot":0.78,"fir":1.0},
        "l14d": {"orders_total":1199,"dt":15.7,"rat":0.9,"tv":3.2,"l10":0.04,"l5":0.15,"tc":2.2,"avtc":5.1,"ot":0.85,"fir":1.0},
        "l7d":  {"orders_total":1223,"dt":15.7,"rat":0.9,"tv":3.1,"l10":0.04,"l5":0.15,"tc":2.2,"avtc":5.1,"ot":0.85,"fir":1.0},
        "l3d":  {"orders_total":1226,"dt":15.6,"rat":1.0,"tv":3.0,"l10":0.03,"l5":0.15,"tc":2.1,"avtc":5.0,"ot":0.85,"fir":1.0},
        "yday": {"orders_total":1333,"dt":16.3,"rat":0.9,"tv":3.3,"l10":0.04,"l5":0.16,"tc":2.2,"avtc":5.3,"ot":0.84,"fir":1.0},
    },
}

with open('/tmp/nasr-city-ops/dashboard_data.json') as f:
    d = json.load(f)

# Map sheet periods to dashboard periods
# Sheet: yday, l3d, l7d, l14d, mtd, lm
# Dashboard perf keys: yday, l3d, l7d, l14d, mtd, lm
period_map = {
    'yday': 'yday',
    'l3d':  'l3d',
    'l7d':  'l7d',
    'l14d': 'l14d',
    'mtd':  'mtd',
    'lm':   'lm',
}

perf = {}
for period_sheet, period_dash in period_map.items():
    perf[period_dash] = {}
    for vc, store_data in PERF_DATA.items():
        perf[period_dash][vc] = store_data[period_sheet]

d['perf'] = perf
with open('/tmp/nasr-city-ops/dashboard_data.json', 'w') as f:
    json.dump(d, f, indent=2)

print("Updated perf section with", len(PERF_DATA), "stores x", len(period_map), "periods")
for vc, sd in PERF_DATA.items():
    print(f"  {vc}: yday dt={sd['yday']['dt']} orders={sd['yday']['orders_total']}")
