#!/usr/bin/env python3
"""Update hybrid section — correct source: fct_logistics_order filtered by sp_id."""
import json
from pathlib import Path

def r4(v): return round(float(v), 4)

# YDAY (2026-08-30) — sp_id filter on fct_logistics_order
yday_orders = {
    10186: {"orders":1422,"dt":11.916,"tv":0.850,"tc":5.161,"rat":0.545,"onTime":0.9571},
    10196: {"orders":1767,"dt":16.028,"tv":1.182,"tc":7.088,"rat":0.852,"onTime":0.9117},
    10198: {"orders":1825,"dt":12.254,"tv":0.828,"tc":5.351,"rat":0.667,"onTime":0.9490},
    10216: {"orders": 819,"dt":16.460,"tv":0.878,"tc":6.741,"rat":0.778,"onTime":0.8864},
    10218: {"orders":2129,"dt":10.842,"tv":0.426,"tc":4.834,"rat":0.406,"onTime":0.9582},
    10219: {"orders": 728,"dt":23.906,"tv":1.396,"tc":9.711,"rat":1.772,"onTime":0.7967},
    10229: {"orders": 325,"dt":17.094,"tv":1.537,"tc":6.911,"rat":1.052,"onTime":0.8831},
    10230: {"orders": 696,"dt":15.346,"tv":0.977,"tc":5.602,"rat":1.023,"onTime":0.9310},
}

# WTD (2026-08-24 to 2026-08-30)
wtd_orders = {
    10186: {"orders": 7361,"dt":11.603,"tv":0.599,"tc":5.232,"rat":0.371,"onTime":0.9599},
    10196: {"orders":10949,"dt":14.688,"tv":0.876,"tc":6.781,"rat":0.569,"onTime":0.9255},
    10198: {"orders":11295,"dt":11.297,"tv":0.548,"tc":5.034,"rat":0.510,"onTime":0.9599},
    10216: {"orders": 5047,"dt":15.793,"tv":0.719,"tc":6.448,"rat":0.908,"onTime":0.8982},
    10218: {"orders":12150,"dt":10.441,"tv":0.295,"tc":4.713,"rat":0.306,"onTime":0.9624},
    10219: {"orders": 4474,"dt":22.548,"tv":1.512,"tc":9.852,"rat":1.861,"onTime":0.8308},
    10229: {"orders": 2231,"dt":16.024,"tv":1.196,"tc":6.567,"rat":0.933,"onTime":0.8965},
    10230: {"orders": 4808,"dt":13.132,"tv":0.790,"tc":5.395,"rat":0.655,"onTime":0.9447},
}

# MTD (2026-08-01 to 2026-08-30)
mtd_orders = {
    10186: {"orders":35812,"dt":11.726,"tv":0.652,"tc":5.482,"rat":0.430,"onTime":0.6705},
    10196: {"orders":46692,"dt":15.989,"tv":1.068,"tc":7.226,"rat":0.850,"onTime":0.9126},
    10198: {"orders":48989,"dt":12.277,"tv":0.825,"tc":5.605,"rat":0.742,"onTime":0.9456},
    10216: {"orders":20662,"dt":16.386,"tv":0.803,"tc":6.978,"rat":1.156,"onTime":0.9003},
    10218: {"orders":56800,"dt":11.049,"tv":0.502,"tc":5.029,"rat":0.497,"onTime":0.9593},
    10219: {"orders":20898,"dt":20.756,"tv":1.559,"tc":9.743,"rat":1.934,"onTime":0.8482},
    10229: {"orders":10588,"dt":16.401,"tv":1.443,"tc":6.862,"rat":1.162,"onTime":0.9110},
    10230: {"orders":19874,"dt":14.892,"tv":0.955,"tc":5.835,"rat":1.050,"onTime":0.9228},
}

# SHIFT METRICS (fct_logistics_rider_shift, shift_start_lt_date)
yday_shift = {
    10186: {"actHrs":579.646,"planHrs":607.000,"riders":46,"noShow":0.0612,"lateLogin":0.2653,"breakMin":6.235},
    10196: {"actHrs":892.444,"planHrs":1005.079,"riders":72,"noShow":0.0741,"lateLogin":0.3704,"breakMin":12.724},
    10198: {"actHrs":850.268,"planHrs":960.748,"riders":69,"noShow":0.1026,"lateLogin":0.3718,"breakMin":16.838},
    10216: {"actHrs":400.908,"planHrs":437.878,"riders":34,"noShow":0.0541,"lateLogin":0.1892,"breakMin":27.728},
    10218: {"actHrs":952.056,"planHrs":1079.728,"riders":73,"noShow":0.0723,"lateLogin":0.4940,"breakMin":12.554},
    10219: {"actHrs":416.698,"planHrs":421.183,"riders":35,"noShow":0.0000,"lateLogin":0.2500,"breakMin":15.138},
    10229: {"actHrs":219.825,"planHrs":291.548,"riders":22,"noShow":0.1538,"lateLogin":0.3462,"breakMin":60.260},
    10230: {"actHrs":335.167,"planHrs":372.000,"riders":29,"noShow":0.0323,"lateLogin":0.2903,"breakMin":32.841},
}
wtd_shift = {
    10186: {"actHrs":3576.257,"planHrs":3916.981,"riders":59,"noShow":0.0123,"lateLogin":0.3466,"breakMin":13.090},
    10196: {"actHrs":5770.366,"planHrs":6181.182,"riders":90,"noShow":0.0394,"lateLogin":0.3642,"breakMin":12.780},
    10198: {"actHrs":5736.368,"planHrs":6121.676,"riders":89,"noShow":0.0286,"lateLogin":0.4898,"breakMin":25.068},
    10216: {"actHrs":2498.897,"planHrs":2661.451,"riders":39,"noShow":0.0046,"lateLogin":0.2431,"breakMin":16.896},
    10218: {"actHrs":6036.216,"planHrs":6531.201,"riders":91,"noShow":0.0352,"lateLogin":0.4814,"breakMin":15.388},
    10219: {"actHrs":2412.784,"planHrs":2621.280,"riders":40,"noShow":0.0192,"lateLogin":0.2468,"breakMin":14.093},
    10229: {"actHrs":1453.029,"planHrs":1937.729,"riders":29,"noShow":0.0983,"lateLogin":0.4162,"breakMin":39.744},
    10230: {"actHrs":2080.570,"planHrs":2300.069,"riders":35,"noShow":0.0366,"lateLogin":0.3455,"breakMin":27.223},
}
mtd_shift = {
    10186: {"actHrs":16927.485,"planHrs":18464.819,"riders":88,"noShow":0.0329,"lateLogin":0.3041,"breakMin":12.061},
    10196: {"actHrs":23359.963,"planHrs":25349.958,"riders":133,"noShow":0.0498,"lateLogin":0.3350,"breakMin":9.941},
    10198: {"actHrs":22999.574,"planHrs":25623.399,"riders":146,"noShow":0.0378,"lateLogin":0.3695,"breakMin":21.856},
    10216: {"actHrs": 9890.363,"planHrs":10899.726,"riders":59,"noShow":0.0450,"lateLogin":0.2521,"breakMin":14.250},
    10218: {"actHrs":25704.091,"planHrs":28134.753,"riders":142,"noShow":0.0364,"lateLogin":0.4117,"breakMin":13.724},
    10219: {"actHrs":10862.761,"planHrs":12165.532,"riders":66,"noShow":0.0345,"lateLogin":0.2573,"breakMin":18.894},
    10229: {"actHrs": 6202.759,"planHrs": 8370.550,"riders":57,"noShow":0.1151,"lateLogin":0.3915,"breakMin":27.739},
    10230: {"actHrs": 9155.114,"planHrs":10561.258,"riders":61,"noShow":0.0619,"lateLogin":0.3794,"breakMin":31.179},
}

def build(orders_d, shift_d):
    out = {}
    for sp, o in orders_d.items():
        s = shift_d[sp]
        ah, riders, orders = s["actHrs"], s["riders"], o["orders"]
        out[str(sp)] = {
            "utr":      r4(orders / ah) if ah > 0 else 0,
            "dt":       r4(o["dt"]),
            "onTime":   r4(o["onTime"]),
            "orders":   orders,
            "riders":   riders,
            "actHrs":   r4(ah),
            "planHrs":  r4(s["planHrs"]),
            "avgHrs":   r4(ah / riders) if riders > 0 else 0,
            "noShow":   r4(s["noShow"]),
            "lateLogin":r4(s["lateLogin"]),
            "breakMin": r4(s["breakMin"]),
            "rat":      r4(o["rat"]),
            "tv":       r4(o["tv"]),
            "tc":       r4(o["tc"]),
        }
    return out

JSON_PATH = Path("/tmp/nasr-city-ops/dashboard_data.json")
with open(JSON_PATH) as f:
    data = json.load(f)

data["hybrid"]["yday"] = build(yday_orders, yday_shift)
data["hybrid"]["wtd"]  = build(wtd_orders,  wtd_shift)
data["hybrid"]["mtd"]  = build(mtd_orders,  mtd_shift)

with open(JSON_PATH, "w") as f:
    json.dump(data, f, indent=2)

print("✅ hybrid updated with correct sp_id-filtered order data")
for period, pd in [("yday", data["hybrid"]["yday"]), ("wtd", data["hybrid"]["wtd"]), ("mtd", data["hybrid"]["mtd"])]:
    print(f"\n{period.upper()}:")
    for sp in ["10186","10196","10198","10216","10218","10219","10229","10230"]:
        d = pd[sp]
        print(f"  {sp}: orders={d['orders']:>6}  dt={d['dt']:>5.1f}  utr={d['utr']:.3f}  riders={d['riders']}")
