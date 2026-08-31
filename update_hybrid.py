#!/usr/bin/env python3
"""Update hybrid section of dashboard_data.json with fresh Looker data (Aug 30, 2026)."""
import json
from pathlib import Path

def r4(v): return round(float(v), 4)

VC_TO_SP = {
    "619844": 10196, "620008": 10186, "655461": 10219, "717765": 10230,
    "760059": 10216, "783048": 10218, "793636": 10198, "801850": 10229,
}

yday_orders_raw = [
    {"vc":"619844","orders":3022,"dt":16.828,"tv":1.636,"tc":7.502,"rat":0.907,"onTime":0.9183},
    {"vc":"620008","orders":1780,"dt":12.103,"tv":1.170,"tc":5.171,"rat":0.585,"onTime":0.9545},
    {"vc":"655461","orders":2553,"dt":26.865,"tv":2.720,"tc":10.328,"rat":2.665,"onTime":0.7770},
    {"vc":"717765","orders":2912,"dt":17.305,"tv":0.737,"tc":8.065,"rat":0.926,"onTime":0.9349},
    {"vc":"760059","orders":2268,"dt":16.497,"tv":1.121,"tc":7.118,"rat":0.714,"onTime":0.9045},
    {"vc":"783048","orders":2541,"dt":11.549,"tv":0.746,"tc":5.077,"rat":0.518,"onTime":0.9534},
    {"vc":"793636","orders":2356,"dt":12.672,"tv":1.234,"tc":5.485,"rat":0.755,"onTime":0.9439},
    {"vc":"801850","orders":1352,"dt":16.380,"tv":2.273,"tc":6.604,"rat":0.959,"onTime":0.9268},
]
wtd_orders_raw = [
    {"vc":"619844","orders":17190,"dt":16.000,"tv":1.606,"tc":7.416,"rat":0.699,"onTime":0.9255},
    {"vc":"620008","orders":9145,"dt":12.163,"tv":0.944,"tc":5.315,"rat":0.493,"onTime":0.9515},
    {"vc":"655461","orders":15425,"dt":24.959,"tv":2.595,"tc":10.433,"rat":2.750,"onTime":0.8169},
    {"vc":"717765","orders":16336,"dt":15.874,"tv":0.834,"tc":7.915,"rat":0.771,"onTime":0.9392},
    {"vc":"760059","orders":11858,"dt":16.599,"tv":1.641,"tc":7.091,"rat":1.063,"onTime":0.9066},
    {"vc":"783048","orders":14539,"dt":11.113,"tv":0.633,"tc":5.031,"rat":0.370,"onTime":0.9575},
    {"vc":"793636","orders":13470,"dt":11.726,"tv":0.900,"tc":5.145,"rat":0.555,"onTime":0.9549},
    {"vc":"801850","orders":7325,"dt":15.869,"tv":2.136,"tc":6.467,"rat":0.917,"onTime":0.9256},
]
mtd_orders_raw = [
    {"vc":"619844","orders":83100,"dt":17.842,"tv":2.158,"tc":7.821,"rat":1.149,"onTime":0.9058},
    {"vc":"620008","orders":45113,"dt":12.445,"tv":1.098,"tc":5.582,"rat":0.647,"onTime":0.6924},
    {"vc":"655461","orders":69552,"dt":23.254,"tv":2.667,"tc":10.396,"rat":2.675,"onTime":0.8302},
    {"vc":"717765","orders":77371,"dt":18.270,"tv":1.702,"tc":8.438,"rat":1.228,"onTime":0.9137},
    {"vc":"760059","orders":57214,"dt":17.473,"tv":1.845,"tc":7.502,"rat":1.490,"onTime":0.9008},
    {"vc":"783048","orders":71159,"dt":11.996,"tv":0.973,"tc":5.410,"rat":0.647,"onTime":0.9523},
    {"vc":"793636","orders":64665,"dt":13.166,"tv":1.493,"tc":5.792,"rat":0.907,"onTime":0.9360},
    {"vc":"801850","orders":35177,"dt":17.161,"tv":2.786,"tc":6.720,"rat":1.416,"onTime":0.9227},
]

yday_shift_raw = [
    {"sp":10186,"actHrs":579.646,"planHrs":607.000,"riders":46,"noShow":0.0612,"lateLogin":0.2653,"breakMin":6.235},
    {"sp":10196,"actHrs":892.444,"planHrs":1005.079,"riders":72,"noShow":0.0741,"lateLogin":0.3704,"breakMin":12.724},
    {"sp":10198,"actHrs":850.268,"planHrs":960.748,"riders":69,"noShow":0.1026,"lateLogin":0.3718,"breakMin":16.838},
    {"sp":10216,"actHrs":400.908,"planHrs":437.878,"riders":34,"noShow":0.0541,"lateLogin":0.1892,"breakMin":27.728},
    {"sp":10218,"actHrs":952.056,"planHrs":1079.728,"riders":73,"noShow":0.0723,"lateLogin":0.4940,"breakMin":12.554},
    {"sp":10219,"actHrs":416.698,"planHrs":421.183,"riders":35,"noShow":0.0000,"lateLogin":0.2500,"breakMin":15.138},
    {"sp":10229,"actHrs":219.825,"planHrs":291.548,"riders":22,"noShow":0.1538,"lateLogin":0.3462,"breakMin":60.260},
    {"sp":10230,"actHrs":335.167,"planHrs":372.000,"riders":29,"noShow":0.0323,"lateLogin":0.2903,"breakMin":32.841},
]
wtd_shift_raw = [
    {"sp":10186,"actHrs":3576.257,"planHrs":3916.981,"riders":59,"noShow":0.0123,"lateLogin":0.3466,"breakMin":13.090},
    {"sp":10196,"actHrs":5770.366,"planHrs":6181.182,"riders":90,"noShow":0.0394,"lateLogin":0.3642,"breakMin":12.780},
    {"sp":10198,"actHrs":5736.368,"planHrs":6121.676,"riders":89,"noShow":0.0286,"lateLogin":0.4898,"breakMin":25.068},
    {"sp":10216,"actHrs":2498.897,"planHrs":2661.451,"riders":39,"noShow":0.0046,"lateLogin":0.2431,"breakMin":16.896},
    {"sp":10218,"actHrs":6036.216,"planHrs":6531.201,"riders":91,"noShow":0.0352,"lateLogin":0.4814,"breakMin":15.388},
    {"sp":10219,"actHrs":2412.784,"planHrs":2621.280,"riders":40,"noShow":0.0192,"lateLogin":0.2468,"breakMin":14.093},
    {"sp":10229,"actHrs":1453.029,"planHrs":1937.729,"riders":29,"noShow":0.0983,"lateLogin":0.4162,"breakMin":39.744},
    {"sp":10230,"actHrs":2080.570,"planHrs":2300.069,"riders":35,"noShow":0.0366,"lateLogin":0.3455,"breakMin":27.223},
]
mtd_shift_raw = [
    {"sp":10186,"actHrs":16927.485,"planHrs":18464.819,"riders":88,"noShow":0.0329,"lateLogin":0.3041,"breakMin":12.061},
    {"sp":10196,"actHrs":23359.963,"planHrs":25349.958,"riders":133,"noShow":0.0498,"lateLogin":0.3350,"breakMin":9.941},
    {"sp":10198,"actHrs":22999.574,"planHrs":25623.399,"riders":146,"noShow":0.0378,"lateLogin":0.3695,"breakMin":21.856},
    {"sp":10216,"actHrs":9890.363,"planHrs":10899.726,"riders":59,"noShow":0.0450,"lateLogin":0.2521,"breakMin":14.250},
    {"sp":10218,"actHrs":25704.091,"planHrs":28134.753,"riders":142,"noShow":0.0364,"lateLogin":0.4117,"breakMin":13.724},
    {"sp":10219,"actHrs":10862.761,"planHrs":12165.532,"riders":66,"noShow":0.0345,"lateLogin":0.2573,"breakMin":18.894},
    {"sp":10229,"actHrs":6202.759,"planHrs":8370.550,"riders":57,"noShow":0.1151,"lateLogin":0.3915,"breakMin":27.739},
    {"sp":10230,"actHrs":9155.114,"planHrs":10561.258,"riders":61,"noShow":0.0619,"lateLogin":0.3794,"breakMin":31.179},
]

def build_period(orders_list, shift_list):
    sidx = {r["sp"]: r for r in shift_list}
    out = {}
    for o in orders_list:
        sp = VC_TO_SP[o["vc"]]
        s = sidx[sp]
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

data["hybrid"]["yday"] = build_period(yday_orders_raw, yday_shift_raw)
data["hybrid"]["wtd"]  = build_period(wtd_orders_raw,  wtd_shift_raw)
data["hybrid"]["mtd"]  = build_period(mtd_orders_raw,  mtd_shift_raw)

with open(JSON_PATH, "w") as f:
    json.dump(data, f, indent=2)

print("✅ hybrid section updated")
for sp in ["10186","10196","10218","10219","10229"]:
    print(f"  YDAY {sp}: orders={data['hybrid']['yday'][sp]['orders']} dt={data['hybrid']['yday'][sp]['dt']} utr={data['hybrid']['yday'][sp]['utr']}")
