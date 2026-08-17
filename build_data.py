import json
from datetime import datetime

# ============================================================
# ALL COLLECTED DATA
# ============================================================

# ---- ZONE DATA (Looker fallback for Tableau) ----
zone_yday = {
    "Nasr city": {"riders":1914,"orders":30924,"delivTime":21.96,"rat":5.285,"toVendor":2.641,
                  "onTime":0.8799,"failRate":0.0201,"sumHrs":15868.3,"plannedHrs":19022.4,
                  "lateLogin":0.0688,"breakMin":53.05,"acceptRate":0.8342,"noShow":0.0018},
    "Heliopolis": {"riders":1802,"orders":28650,"delivTime":22.13,"rat":6.173,"toVendor":3.198,
                   "onTime":0.8391,"failRate":0.0180,"sumHrs":13362.5,"plannedHrs":16461.5,
                   "lateLogin":0.0766,"breakMin":52.31,"acceptRate":0.8117,"noShow":0.0},
    "Ain shams": {"riders":403,"orders":4983,"delivTime":24.13,"rat":6.436,"toVendor":4.174,
                  "onTime":0.7922,"failRate":0.0252,"sumHrs":2353.7,"plannedHrs":2982.1,
                  "lateLogin":0.0613,"breakMin":38.50,"acceptRate":0.7893,"noShow":0.0},
}

zone_wtd = {
    "Nasr city": {"riders":2714,"orders":217509,"delivTime":22.056,"rat":6.420,"toVendor":3.075,
                  "onTime":0.8608,"failRate":0.0233,"sumHrs":109561.5,"plannedHrs":129004.1,
                  "lateLogin":0.0612,"breakMin":51.67,"acceptRate":0.8493,"noShow":0.0307},
    "Heliopolis": {"riders":2887,"orders":194758,"delivTime":21.845,"rat":7.404,"toVendor":3.264,
                   "onTime":0.7945,"failRate":0.0243,"sumHrs":92227.1,"plannedHrs":113357.7,
                   "lateLogin":0.0675,"breakMin":51.59,"acceptRate":0.8136,"noShow":0.0590},
    "Ain shams": {"riders":798,"orders":34127,"delivTime":23.654,"rat":6.812,"toVendor":3.972,
                  "onTime":0.7805,"failRate":0.0293,"sumHrs":17023.2,"plannedHrs":20957.2,
                  "lateLogin":0.0642,"breakMin":36.56,"acceptRate":0.8123,"noShow":0.0437},
}

zone_mtd = {
    "Nasr city": {"riders":3365,"orders":495823,"delivTime":22.409,"rat":6.807,"toVendor":3.311,
                  "onTime":0.8543,"failRate":0.0238,"sumHrs":250426.0,"plannedHrs":294866.0,
                  "lateLogin":0.0612,"breakMin":51.67,"acceptRate":0.8493,"noShow":0.0356},
    "Heliopolis": {"riders":3741,"orders":450900,"delivTime":22.019,"rat":6.783,"toVendor":3.287,
                   "onTime":0.8184,"failRate":0.0223,"sumHrs":210804.0,"plannedHrs":259104.0,
                   "lateLogin":0.0675,"breakMin":51.59,"acceptRate":0.8136,"noShow":0.0642},
    "Ain shams": {"riders":1177,"orders":79434,"delivTime":24.042,"rat":6.472,"toVendor":4.048,
                  "onTime":0.7881,"failRate":0.0326,"sumHrs":38910.0,"plannedHrs":47916.0,
                  "lateLogin":0.0642,"breakMin":36.56,"acceptRate":0.8123,"noShow":0.0499},
}

# ---- DTC (carry forward from existing) ----
dtc_yday = {"ard_golf":[89.0,0,0],"hegaz":[68.0,0,0],"matareya":[33.0,0,0],
            "hadeeqa":[88.0,0,0],"tayaran":[54.0,0,0],"hay8":[57.0,0,0],
            "shorouk":[81.0,0,0],"omarat":[61.0,0,0]}
dtc_mtd = {"ard_golf":[82.1,0,0],"hegaz":[55.2,0,0],"matareya":[32.5,0,0],
           "hadeeqa":[81.1,0,0],"tayaran":[46.5,0,0],"hay8":[43.1,0,0],
           "shorouk":[72.1,0,0],"masaken_sh":[51.9,0,0],"omarat":[49.6,0,0]}

# ---- OFFENDERS (carry forward existing) ----
offenders = {"Nasr city":[{"id":4811704,"noShow":7,"late":0,"breaks":0.0,"avp":0.0,"shifts":7},{"id":4811635,"noShow":7,"late":0,"breaks":0.0,"avp":0.0,"shifts":7},{"id":4765718,"noShow":7,"late":0,"breaks":0.0,"avp":0.0,"shifts":7},{"id":4808104,"noShow":7,"late":0,"breaks":0.0,"avp":0.0,"shifts":7},{"id":4812562,"noShow":7,"late":0,"breaks":0.0,"avp":0.0,"shifts":7},{"id":2160437,"noShow":7,"late":0,"breaks":0.0,"avp":0.0,"shifts":7},{"id":4810407,"noShow":7,"late":0,"breaks":2.0,"avp":3.8,"shifts":9},{"id":2070739,"noShow":6,"late":0,"breaks":10.9,"avp":33.9,"shifts":13},{"id":4809263,"noShow":6,"late":0,"breaks":0.0,"avp":0.0,"shifts":6},{"id":4712851,"noShow":6,"late":0,"breaks":0.0,"avp":0.0,"shifts":6},{"id":2497581,"noShow":6,"late":0,"breaks":2.8,"avp":14.0,"shifts":8},{"id":4594352,"noShow":6,"late":0,"breaks":0.0,"avp":0.0,"shifts":6},{"id":4710477,"noShow":6,"late":0,"breaks":2.2,"avp":5.6,"shifts":7},{"id":4707745,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":3674158,"noShow":5,"late":0,"breaks":3.2,"avp":28.6,"shifts":9},{"id":4783424,"noShow":5,"late":2,"breaks":3.9,"avp":27.7,"shifts":9},{"id":4472110,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":1780112,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":4591503,"noShow":5,"late":3,"breaks":14.2,"avp":33.4,"shifts":17},{"id":4813855,"noShow":5,"late":1,"breaks":5.0,"avp":18.3,"shifts":8},{"id":4337254,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":4559589,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":4654155,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":2156061,"noShow":4,"late":0,"breaks":0.0,"avp":38.9,"shifts":6},{"id":4722464,"noShow":4,"late":1,"breaks":10.4,"avp":31.9,"shifts":7},{"id":2269368,"noShow":4,"late":0,"breaks":0.6,"avp":24.2,"shifts":5},{"id":4752436,"noShow":4,"late":1,"breaks":1.3,"avp":38.3,"shifts":6},{"id":3529157,"noShow":4,"late":1,"breaks":3.2,"avp":30.5,"shifts":6},{"id":2834196,"noShow":4,"late":0,"breaks":0.0,"avp":0.0,"shifts":4},{"id":4764497,"noShow":4,"late":1,"breaks":7.6,"avp":14.6,"shifts":11},{"id":4265605,"noShow":4,"late":2,"breaks":2.6,"avp":17.3,"shifts":6},{"id":2127148,"noShow":4,"late":1,"breaks":6.3,"avp":2.5,"shifts":5},{"id":3926637,"noShow":4,"late":0,"breaks":1.4,"avp":51.5,"shifts":10},{"id":4691849,"noShow":4,"late":0,"breaks":8.4,"avp":20.2,"shifts":7},{"id":4140034,"noShow":4,"late":0,"breaks":0.0,"avp":0.0,"shifts":4},{"id":2023378,"noShow":4,"late":7,"breaks":17.4,"avp":40.2,"shifts":11},{"id":4754402,"noShow":4,"late":5,"breaks":10.6,"avp":32.2,"shifts":11},{"id":2154584,"noShow":4,"late":5,"breaks":4.4,"avp":32.0,"shifts":9},{"id":4689417,"noShow":4,"late":2,"breaks":3.8,"avp":24.4,"shifts":8},{"id":4783235,"noShow":4,"late":2,"breaks":4.1,"avp":62.6,"shifts":13},{"id":1052863,"noShow":4,"late":5,"breaks":0.5,"avp":42.5,"shifts":9},{"id":4815867,"noShow":4,"late":3,"breaks":1.0,"avp":51.3,"shifts":10},{"id":4182887,"noShow":4,"late":2,"breaks":13.7,"avp":18.7,"shifts":8},{"id":4807891,"noShow":4,"late":0,"breaks":1.0,"avp":18.3,"shifts":5},{"id":4576403,"noShow":4,"late":5,"breaks":11.3,"avp":37.4,"shifts":14},{"id":4810503,"noShow":4,"late":7,"breaks":13.9,"avp":21.4,"shifts":13}],"Heliopolis":[{"id":4769937,"noShow":8,"late":1,"breaks":2.8,"avp":3.3,"shifts":9},{"id":4133861,"noShow":7,"late":0,"breaks":0.0,"avp":0.0,"shifts":7},{"id":4406017,"noShow":7,"late":2,"breaks":1.3,"avp":11.9,"shifts":9},{"id":4549182,"noShow":7,"late":3,"breaks":14.5,"avp":11.6,"shifts":11},{"id":1929761,"noShow":6,"late":0,"breaks":0.0,"avp":0.0,"shifts":6},{"id":4806991,"noShow":6,"late":1,"breaks":0.2,"avp":17.3,"shifts":7},{"id":2495115,"noShow":6,"late":0,"breaks":4.8,"avp":13.9,"shifts":9},{"id":4242600,"noShow":6,"late":0,"breaks":0.0,"avp":0.0,"shifts":6},{"id":4783389,"noShow":6,"late":2,"breaks":6.1,"avp":35.0,"shifts":12},{"id":4809245,"noShow":6,"late":0,"breaks":0.0,"avp":0.0,"shifts":6},{"id":4689551,"noShow":6,"late":0,"breaks":0.0,"avp":0.0,"shifts":6},{"id":4783648,"noShow":6,"late":0,"breaks":4.0,"avp":12.5,"shifts":7},{"id":4813713,"noShow":6,"late":2,"breaks":1.0,"avp":9.9,"shifts":9},{"id":4815364,"noShow":5,"late":1,"breaks":0.6,"avp":27.1,"shifts":7},{"id":2140297,"noShow":5,"late":0,"breaks":0.8,"avp":28.1,"shifts":7},{"id":653631,"noShow":5,"late":0,"breaks":1.0,"avp":11.2,"shifts":6},{"id":2172819,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":1110676,"noShow":5,"late":2,"breaks":12.1,"avp":0.2,"shifts":9},{"id":1285640,"noShow":5,"late":0,"breaks":5.9,"avp":3.3,"shifts":8},{"id":4523344,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":4769673,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":4614846,"noShow":5,"late":0,"breaks":5.3,"avp":5.7,"shifts":6},{"id":4202995,"noShow":5,"late":0,"breaks":5.0,"avp":14.8,"shifts":7},{"id":3968316,"noShow":5,"late":1,"breaks":15.6,"avp":11.1,"shifts":7},{"id":1235541,"noShow":5,"late":0,"breaks":1.7,"avp":32.0,"shifts":7},{"id":1798369,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":4813460,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":4761241,"noShow":5,"late":2,"breaks":5.5,"avp":13.5,"shifts":8},{"id":2112167,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":4803759,"noShow":5,"late":0,"breaks":0.0,"avp":0.0,"shifts":5},{"id":2272649,"noShow":5,"late":0,"breaks":2.2,"avp":14.0,"shifts":6},{"id":3529074,"noShow":5,"late":2,"breaks":1.0,"avp":22.8,"shifts":7},{"id":1141607,"noShow":4,"late":0,"breaks":12.1,"avp":59.0,"shifts":16},{"id":4802826,"noShow":4,"late":0,"breaks":0.5,"avp":2.8,"shifts":5},{"id":4340695,"noShow":4,"late":2,"breaks":8.5,"avp":15.6,"shifts":6},{"id":4609581,"noShow":4,"late":3,"breaks":6.6,"avp":49.2,"shifts":13},{"id":4653485,"noShow":4,"late":0,"breaks":1.5,"avp":3.1,"shifts":5},{"id":1132254,"noShow":4,"late":2,"breaks":3.6,"avp":31.9,"shifts":9},{"id":2516497,"noShow":4,"late":0,"breaks":0.0,"avp":29.3,"shifts":5},{"id":4775556,"noShow":4,"late":4,"breaks":5.5,"avp":26.4,"shifts":8},{"id":1390508,"noShow":4,"late":0,"breaks":0.0,"avp":0.0,"shifts":4},{"id":4811744,"noShow":4,"late":0,"breaks":0.8,"avp":25.1,"shifts":6},{"id":4409100,"noShow":4,"late":0,"breaks":6.7,"avp":43.0,"shifts":10},{"id":4666733,"noShow":4,"late":1,"breaks":6.2,"avp":21.6,"shifts":7},{"id":2402774,"noShow":4,"late":5,"breaks":0.2,"avp":34.2,"shifts":9},{"id":4264541,"noShow":4,"late":0,"breaks":7.3,"avp":37.6,"shifts":8},{"id":3871383,"noShow":4,"late":0,"breaks":0.0,"avp":0.0,"shifts":4},{"id":2402693,"noShow":4,"late":1,"breaks":0.6,"avp":24.9,"shifts":6},{"id":4611674,"noShow":4,"late":0,"breaks":5.7,"avp":35.2,"shifts":7},{"id":4755127,"noShow":4,"late":0,"breaks":0.0,"avp":0.0,"shifts":4}],"Ain shams":[{"id":3991650,"noShow":6,"late":0,"breaks":4.3,"avp":19.4,"shifts":9},{"id":4809195,"noShow":6,"late":2,"breaks":1.5,"avp":8.1,"shifts":8},{"id":4783169,"noShow":5,"late":2,"breaks":4.9,"avp":21.4,"shifts":9},{"id":4642949,"noShow":5,"late":2,"breaks":2.1,"avp":46.6,"shifts":7},{"id":3925170,"noShow":4,"late":0,"breaks":0.2,"avp":9.9,"shifts":5},{"id":4010909,"noShow":4,"late":0,"breaks":0.0,"avp":37.9,"shifts":6},{"id":4783233,"noShow":4,"late":1,"breaks":7.9,"avp":9.2,"shifts":7},{"id":1623967,"noShow":4,"late":0,"breaks":0.5,"avp":24.3,"shifts":6},{"id":4804487,"noShow":4,"late":3,"breaks":14.9,"avp":32.6,"shifts":11},{"id":4280168,"noShow":4,"late":0,"breaks":2.5,"avp":43.2,"shifts":7},{"id":4775489,"noShow":4,"late":1,"breaks":1.3,"avp":20.5,"shifts":5}]}

# ---- HYBRID SPs (carry forward yday/wtd/mtd due to SP data lag) ----
hybrid_yday = {"10186":{"riders":49,"actHrs":590.2,"planHrs":627.89,"orders":1267,"dt":10.4,"rat":0.27,"tv":0.48,"tc":5.1,"onTime":0.4538,"noShow":0.0395,"lateLogin":0.0192,"breakMin":12.45},"10196":{"riders":63,"actHrs":736.87,"planHrs":752.9,"orders":1418,"dt":16.47,"rat":0.86,"tv":1.28,"tc":7.61,"onTime":0.9041,"noShow":0.011,"lateLogin":0.0909,"breakMin":17.96},"10198":{"riders":63,"actHrs":774.08,"planHrs":831.49,"orders":1671,"dt":11.29,"rat":0.57,"tv":0.74,"tc":5.45,"onTime":0.9569,"noShow":0.0417,"lateLogin":0.0571,"breakMin":18.77},"10216":{"riders":0,"actHrs":50.67,"planHrs":58.13,"orders":0,"dt":0.0,"rat":0.0,"tv":0.0,"tc":0.0,"onTime":0.0,"noShow":0.1429,"lateLogin":0.0,"breakMin":0.0},"10218":{"riders":79,"actHrs":1002.55,"planHrs":1070.54,"orders":1972,"dt":9.95,"rat":0.29,"tv":0.35,"tc":4.81,"onTime":0.9696,"noShow":0.0403,"lateLogin":0.0581,"breakMin":12.7},"10219":{"riders":36,"actHrs":404.17,"planHrs":420.6,"orders":788,"dt":20.98,"rat":1.92,"tv":1.68,"tc":10.47,"onTime":0.8376,"noShow":0.0189,"lateLogin":0.0417,"breakMin":18.99},"10229":{"riders":22,"actHrs":231.38,"planHrs":256.0,"orders":425,"dt":15.7,"rat":1.08,"tv":1.37,"tc":6.62,"onTime":0.9341,"noShow":0.0,"lateLogin":0.3043,"breakMin":49.29},"10230":{"riders":28,"actHrs":314.96,"planHrs":357.74,"orders":680,"dt":14.59,"rat":1.22,"tv":1.06,"tc":5.8,"onTime":0.9118,"noShow":0.0488,"lateLogin":0.0,"breakMin":48.56}}

hybrid_wtd = {"10186":{"riders":57,"actHrs":3128.99,"planHrs":3217.4,"orders":6351,"dt":11.02,"rat":0.42,"tv":0.45,"tc":5.44,"onTime":0.4913,"noShow":0.0151,"lateLogin":0.0368,"breakMin":17.44},"10196":{"riders":75,"actHrs":3943.9,"planHrs":4045.82,"orders":7803,"dt":16.62,"rat":1.07,"tv":1.14,"tc":7.67,"onTime":0.904,"noShow":0.0167,"lateLogin":0.0736,"breakMin":8.88},"10198":{"riders":78,"actHrs":3977.64,"planHrs":4258.82,"orders":8523,"dt":12.43,"rat":0.86,"tv":0.85,"tc":5.88,"onTime":0.9372,"noShow":0.0302,"lateLogin":0.0528,"breakMin":21.32},"10216":{"riders":38,"actHrs":1848.5,"planHrs":2004.62,"orders":3437,"dt":16.25,"rat":1.36,"tv":0.79,"tc":7.29,"onTime":0.899,"noShow":0.0378,"lateLogin":0.0944,"breakMin":19.55},"10218":{"riders":89,"actHrs":4867.92,"planHrs":5021.45,"orders":10103,"dt":10.45,"rat":0.43,"tv":0.38,"tc":4.99,"onTime":0.9602,"noShow":0.02,"lateLogin":0.0468,"breakMin":12.68},"10219":{"riders":42,"actHrs":2081.67,"planHrs":2163.29,"orders":3964,"dt":20.16,"rat":2.07,"tv":1.51,"tc":9.65,"onTime":0.8375,"noShow":0.0101,"lateLogin":0.0319,"breakMin":21.75},"10229":{"riders":30,"actHrs":1167.66,"planHrs":1476.03,"orders":2193,"dt":16.95,"rat":1.75,"tv":1.63,"tc":7.24,"onTime":0.9024,"noShow":0.1438,"lateLogin":0.1942,"breakMin":23.59},"10230":{"riders":32,"actHrs":1531.58,"planHrs":1668.85,"orders":3271,"dt":14.47,"rat":1.16,"tv":1.04,"tc":5.85,"onTime":0.9211,"noShow":0.0272,"lateLogin":0.0537,"breakMin":29.56}}

hybrid_mtd = {"10186":{"riders":57,"actHrs":7917.97,"planHrs":8302.2,"orders":7621,"dt":11.22,"rat":0.47,"tv":0.56,"tc":5.51,"onTime":0.5091,"noShow":0.0234,"lateLogin":0.0346,"breakMin":25.58},"10196":{"riders":78,"actHrs":9903.18,"planHrs":10239.14,"orders":9160,"dt":16.67,"rat":1.1,"tv":1.16,"tc":7.72,"onTime":0.9041,"noShow":0.0216,"lateLogin":0.0684,"breakMin":14.6},"10198":{"riders":82,"actHrs":10280.75,"planHrs":10957.87,"orders":9825,"dt":12.57,"rat":0.88,"tv":0.88,"tc":5.93,"onTime":0.9356,"noShow":0.0224,"lateLogin":0.05,"breakMin":31.5},"10216":{"riders":40,"actHrs":4805.01,"planHrs":5179.32,"orders":4111,"dt":16.19,"rat":1.38,"tv":0.79,"tc":7.25,"onTime":0.9027,"noShow":0.0317,"lateLogin":0.0966,"breakMin":25.81},"10218":{"riders":89,"actHrs":12159.77,"planHrs":12618.16,"orders":11658,"dt":10.8,"rat":0.52,"tv":0.49,"tc":5.11,"onTime":0.957,"noShow":0.0207,"lateLogin":0.0413,"breakMin":19.6},"10219":{"riders":42,"actHrs":5044.46,"planHrs":5365.88,"orders":4609,"dt":20.09,"rat":2.06,"tv":1.51,"tc":9.68,"onTime":0.8377,"noShow":0.0204,"lateLogin":0.0278,"breakMin":34.18},"10229":{"riders":32,"actHrs":2585.84,"planHrs":3278.29,"orders":2420,"dt":16.9,"rat":1.71,"tv":1.64,"tc":7.26,"onTime":0.9041,"noShow":0.144,"lateLogin":0.1813,"breakMin":35.4},"10230":{"riders":34,"actHrs":4151.01,"planHrs":4589.34,"orders":3772,"dt":14.91,"rat":1.17,"tv":1.06,"tc":5.94,"onTime":0.917,"noShow":0.0418,"lateLogin":0.0503,"breakMin":38.54}}

# ---- PERF (Tmart vendors) - all new data from Looker ----
def r4(v): return round(float(v), 4)

def perf_row(orders, dt, tv, tc, avtc, ot, l10, l5, fir, rat, failRate=None):
    d = {"orders_total":int(orders),"dt":r4(dt),"rat":r4(rat),"tv":r4(tv),"tc":r4(tc),
         "avtc":r4(avtc),"l10":r4(l10),"l5":r4(l5),"fir":r4(min(fir,1.005)),"ot":r4(ot)}
    return d

perf_yday = {
    "619844": perf_row(2792,21.02,1.952,6.337,5.559,0.9046,0.0304,0.1163,0.9993,1.013),
    "783048": perf_row(2509,15.12,0.974,3.580,2.924,0.9534,0.0083,0.0494,1.0004,0.430),
    "717765": perf_row(2497,20.39,0.758,5.475,4.200,0.9309,0.0234,0.0638,0.9980,0.949),
    "655461": perf_row(2378,23.38,2.879,6.556,6.097,0.8222,0.0998,0.2754,1.0008,2.763),
    "793636": perf_row(2250,16.84,1.739,4.122,3.553,0.9310,0.0340,0.1307,1.0009,0.983),
    "760059": perf_row(2174,22.67,2.425,9.743,9.127,0.8316,0.0970,0.2148,0.9973,2.832),
    "619849": perf_row(1998,18.96,2.054,3.761,3.250,0.7797,0.0493,0.1723,1.0,1.474),
    "620008": perf_row(1581,16.32,1.471,4.012,3.351,0.5996,0.0221,0.0945,1.0013,0.695),
    "801850": perf_row(1206,20.52,2.576,5.436,5.076,0.9401,0.0386,0.1783,1.0008,1.119),
}

perf_l3d = {
    "619844": perf_row(8421,20.83,2.181,6.058,5.363,0.9025,0.0379,0.1425,0.9994,1.156),
    "717765": perf_row(7856,20.36,1.389,5.207,4.134,0.9266,0.0286,0.0814,0.9980,1.118),
    "655461": perf_row(7368,22.97,2.902,6.376,5.969,0.8309,0.0944,0.2641,1.0008,2.845),
    "783048": perf_row(7134,14.79,0.769,3.792,3.015,0.9574,0.0089,0.0446,0.9997,0.433),
    "793636": perf_row(6591,16.12,1.568,3.984,3.399,0.9373,0.0324,0.1168,1.0,0.940),
    "619849": perf_row(6001,18.73,1.825,3.995,3.399,0.7686,0.0388,0.1494,1.0002,1.358),
    "620008": perf_row(4469,15.06,0.970,3.921,3.105,0.5112,0.0156,0.0643,0.9991,0.594),
    "801850": perf_row(3516,19.81,2.596,5.400,5.032,0.9330,0.0516,0.1955,1.0003,1.323),
    "760059": perf_row(2503,22.13,2.430,9.007,8.443,0.8353,0.0980,0.2220,0.9976,2.874),
}

perf_l7d = {
    "619844": perf_row(19886,20.76,2.294,5.759,5.126,0.9003,0.0437,0.1629,0.9999,1.276),
    "717765": perf_row(18056,21.01,1.677,5.469,4.354,0.9155,0.0352,0.1060,0.9986,1.219),
    "783048": perf_row(17092,14.90,0.865,3.820,3.063,0.9574,0.0144,0.0603,0.9992,0.572),
    "655461": perf_row(16247,22.91,2.711,6.230,5.746,0.8240,0.1032,0.2564,1.0021,2.856),
    "793636": perf_row(15547,16.31,1.561,4.072,3.489,0.9329,0.0335,0.1194,0.9990,0.975),
    "619849": perf_row(14316,19.12,2.329,3.822,3.334,0.7824,0.0664,0.2097,1.0005,1.741),
    "760059": perf_row(11316,19.43,1.947,6.165,5.501,0.8763,0.0758,0.1883,1.0010,1.954),
    "620008": perf_row(10825,15.34,1.009,3.988,3.162,0.5373,0.0218,0.0797,0.9996,0.729),
    "801850": perf_row(8476,20.31,2.953,5.298,4.997,0.9063,0.0887,0.2682,1.0019,2.144),
}

perf_l14d = {
    "619844": perf_row(39729,21.23,2.528,5.729,5.190,0.8943,0.0518,0.1901,1.0005,1.477),
    "717765": perf_row(36747,22.41,2.232,6.366,5.145,0.8983,0.0443,0.1267,0.9988,1.553),
    "783048": perf_row(34087,15.20,1.143,3.812,3.176,0.9515,0.0176,0.0809,0.9996,0.801),
    "655461": perf_row(32204,22.87,2.711,5.904,5.404,0.8309,0.0967,0.2488,1.0018,2.698),
    "793636": perf_row(30694,16.80,1.830,4.081,3.579,0.9233,0.0410,0.1448,0.9997,1.165),
    "619849": perf_row(28433,19.26,2.367,3.926,3.456,0.7911,0.0611,0.2108,1.0001,1.803),
    "760059": perf_row(25965,19.17,2.064,5.537,4.932,0.8930,0.0613,0.1804,1.0008,1.954),
    "620008": perf_row(21876,15.50,1.197,3.968,3.267,0.5679,0.0219,0.0854,1.0002,0.774),
    "801850": perf_row(16715,20.52,3.225,5.152,4.905,0.9146,0.0855,0.2887,1.0027,1.927),
}

perf_mtd = {
    "619844": perf_row(45236,21.18,2.502,5.756,5.211,0.8934,0.0520,0.1894,1.0005,1.481),
    "717765": perf_row(42266,22.46,2.245,6.411,5.236,0.8972,0.0463,0.1306,0.9986,1.578),
    "783048": perf_row(39031,15.17,1.129,3.821,3.169,0.9529,0.0177,0.0805,0.9996,0.793),
    "655461": perf_row(36888,22.99,2.717,6.117,5.613,0.8299,0.0983,0.2534,1.0015,2.795),
    "793636": perf_row(35232,16.73,1.811,4.069,3.562,0.9253,0.0405,0.1432,0.9996,1.166),
    "619849": perf_row(32665,19.32,2.281,3.996,3.504,0.7897,0.0584,0.2033,1.0,1.741),
    "760059": perf_row(30202,19.21,2.040,5.570,4.957,0.8950,0.0583,0.1745,1.0006,1.878),
    "620008": perf_row(24901,15.48,1.185,3.967,3.261,0.5670,0.0211,0.0840,1.0003,0.758),
    "801850": perf_row(19183,20.49,3.157,5.174,4.917,0.9175,0.0808,0.2791,1.0025,1.832),
}

perf_lm = {
    "619844": perf_row(82827,20.38,2.584,5.100,4.608,0.9057,0.0534,0.1925,1.0006,1.413),
    "717765": perf_row(75348,22.13,2.032,6.180,5.278,0.9049,0.0445,0.1313,0.9988,1.273),
    "655461": perf_row(68492,23.36,2.471,6.190,5.564,0.8420,0.0753,0.2150,1.0007,2.366),
    "783048": perf_row(67570,16.50,1.833,3.960,3.500,0.9410,0.0304,0.1250,1.0006,1.196),
    "793636": perf_row(62878,16.75,2.043,3.846,3.355,0.9321,0.0459,0.1515,1.0007,1.053),
    "619849": perf_row(60716,19.34,1.966,3.751,3.192,0.7542,0.0442,0.1685,0.9999,1.306),
    "760059": perf_row(60086,19.22,1.945,4.939,4.314,0.9216,0.0375,0.1429,0.9998,1.320),
    "620008": perf_row(44676,17.31,1.849,4.723,4.160,0.7114,0.0325,0.1296,1.0004,1.116),
    "801850": perf_row(33511,20.67,3.134,5.082,4.781,0.9290,0.0686,0.2505,1.0011,1.254),
}

# ---- PERF_SHIFT (SP-level late shift %) ----
# yday
ps_yday = {
    "10229":{"l10":r4(0.2917),"l5":r4(0.2917)},
    "10216":{"l10":r4(0.1111),"l5":r4(0.1111)},
    "10196":{"l10":r4(0.0758),"l5":r4(0.1061)},
    "10198":{"l10":r4(0.0435),"l5":r4(0.0435)},
    "10219":{"l10":r4(0.0417),"l5":r4(0.0625)},
    "10218":{"l10":r4(0.0370),"l5":r4(0.0617)},
    "10230":{"l10":r4(0.0323),"l5":r4(0.0645)},
    "10186":{"l10":r4(0.0196),"l5":r4(0.0588)},
}
# l3d
ps_l3d = {
    "10229":{"l10":r4(0.2778),"l5":r4(0.2917)},
    "10196":{"l10":r4(0.0918),"l5":r4(0.1159)},
    "10218":{"l10":r4(0.0575),"l5":r4(0.0690)},
    "10198":{"l10":r4(0.0550),"l5":r4(0.0688)},
    "10216":{"l10":r4(0.0481),"l5":r4(0.0481)},
    "10219":{"l10":r4(0.0423),"l5":r4(0.0845)},
    "10230":{"l10":r4(0.0323),"l5":r4(0.0430)},
    "10186":{"l10":r4(0.0195),"l5":r4(0.0325)},
}
# l7d/wtd (7-day limit so l14d and mtd return same values)
ps_l7d = {
    "10229":{"l10":r4(0.2204),"l5":r4(0.2312)},
    "10216":{"l10":r4(0.0833),"l5":r4(0.0873)},
    "10196":{"l10":r4(0.0762),"l5":r4(0.0982)},
    "10198":{"l10":r4(0.0521),"l5":r4(0.0734)},
    "10218":{"l10":r4(0.0471),"l5":r4(0.0673)},
    "10230":{"l10":r4(0.0427),"l5":r4(0.0474)},
    "10219":{"l10":r4(0.0349),"l5":r4(0.0640)},
    "10186":{"l10":r4(0.0320),"l5":r4(0.0427)},
}

# ============================================================
# ASSEMBLE dashboard_data.json
# ============================================================
data = {
    "generated": "2026-08-17",
    "data_date": "2026-08-16",
    "tableau_fallback": True,
    "zone": {
        "yday": zone_yday,
        "wtd": zone_wtd,
        "mtd": zone_mtd,
    },
    "dtc_yday": dtc_yday,
    "dtc_mtd": dtc_mtd,
    "offenders": offenders,
    "hybrid": {
        "yday": hybrid_yday,
        "wtd": hybrid_wtd,
        "mtd": hybrid_mtd,
    },
    "perf": {
        "yday": perf_yday,
        "l3d": perf_l3d,
        "l7d": perf_l7d,
        "l14d": perf_l14d,
        "mtd": perf_mtd,
        "lm": perf_lm,
    },
    "perf_shift": {
        "yday": ps_yday,
        "l3d": ps_l3d,
        "l7d": ps_l7d,
        "l14d": ps_l7d,  # same due to 7-day limit
        "mtd": ps_l7d,   # same due to 7-day limit
        "lm": ps_l7d,    # July data empty, use l7d as fallback
    },
}

output_path = "/tmp/nasr-city-ops/dashboard_data.json"
with open(output_path, "w") as f:
    json.dump(data, f, indent=2)
print(f"Written: {output_path}")
print(f"Zones: {list(data['zone']['yday'].keys())}")
print(f"Perf vendors: {list(data['perf']['yday'].keys())}")
print(f"Perf periods: {list(data['perf'].keys())}")
print(f"Perf_shift periods: {list(data['perf_shift'].keys())}")
print(f"Hybrid SPs: {list(data['hybrid']['yday'].keys())}")
