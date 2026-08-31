import json, re

# New fir (cols 60-65: lm,mtd,l14d,l7d,l3d,yday) and tc (cols 76-81) values per VC
# Already confirmed these match the existing "tc" values in update_perf.py for fir
SHEET_DATA = {
    "619844": {"fir":[2.9,3.1,3.1,3.0,3.0,3.1], "avtc":[4.9,4.9,4.5,4.5,4.5,4.8], "tc":[8.0,7.8,7.4,7.3,7.3,7.5]},
    "619849": {"fir":[2.7,3.0,2.9,2.9,2.8,2.8], "avtc":[3.2,3.3,3.2,3.3,3.2,3.2], "tc":[7.8,7.7,7.3,7.1,7.0,7.1]},
    "620008": {"fir":[2.5,2.3,2.4,2.6,2.5,2.7], "avtc":[4.0,3.3,3.4,3.6,3.4,3.3], "tc":[6.1,5.5,5.4,5.3,5.1,5.2]},
    "655461": {"fir":[3.4,3.5,3.9,5.0,6.2,6.9], "avtc":[5.7,5.9,6.2,7.1,8.3,9.5], "tc":[10.3,10.4,10.2,10.4,10.5,10.5]},
    "717765": {"fir":[4.5,4.2,3.1,3.3,3.5,4.1], "avtc":[5.4,4.7,4.1,4.1,4.2,4.7], "tc":[8.7,8.5,8.1,8.0,7.9,8.1]},
    "760059": {"fir":[2.9,3.2,2.9,2.9,2.9,3.2], "avtc":[4.4,5.0,5.0,5.2,5.4,5.7], "tc":[7.7,7.5,7.2,7.1,7.2,7.2]},
    "783048": {"fir":[2.3,2.5,2.6,2.6,2.5,2.6], "avtc":[3.5,3.2,3.2,3.2,3.1,3.2], "tc":[5.8,5.4,5.2,5.1,4.9,5.0]},
    "793636": {"fir":[2.2,2.5,2.5,2.6,2.4,2.5], "avtc":[3.4,3.5,3.4,3.5,3.4,3.5], "tc":[6.0,5.8,5.4,5.2,5.3,5.5]},
    "801850": {"fir":[2.2,2.2,2.2,2.2,2.1,2.2], "avtc":[5.0,5.0,5.1,5.1,5.0,5.3], "tc":[6.8,6.8,6.5,6.6,6.5,6.7]},
}

PERIODS = ['lm','mtd','l14d','l7d','l3d','yday']

# Read current script
with open('/tmp/nasr-city-ops/update_perf.py') as f:
    content = f.read()

# Build a new PERF_DATA by parsing the existing one and patching fir/tc/avtc
# Extract the existing PERF_DATA via exec
exec_globals = {}
exec(content.split('\nwith open')[0], exec_globals)
PERF_DATA = exec_globals['PERF_DATA']

# Patch each vc/period
for vc, sd in SHEET_DATA.items():
    if vc not in PERF_DATA:
        print(f"WARNING: {vc} not in PERF_DATA")
        continue
    for i, period in enumerate(PERIODS):
        d = PERF_DATA[vc][period]
        # The old 'tc' was actually FIR Prep — verify it matches
        old_tc = d.get('tc')
        new_fir = sd['fir'][i]
        if abs((old_tc or 0) - new_fir) > 0.2:
            print(f"  {vc} {period}: old tc={old_tc} vs sheet fir={new_fir} — mismatch!")
        d['fir'] = new_fir
        d['tc']  = sd['tc'][i]
        d['avtc'] = sd['avtc'][i]

# Re-generate the script
lines = ['import json', '', 'PERF_DATA = {']
for vc, periods in PERF_DATA.items():
    lines.append(f'    "{vc}": {{')
    for period, d in periods.items():
        fields = ','.join(f'"{k}":{v}' for k,v in d.items())
        lines.append(f'        "{period}": {{{fields}}},')
    lines.append('    },')
lines.append('}')

# Append the rest of the original script (the json update part)
rest = content.split('\nwith open')[1]
lines.append('\nwith open' + rest)

new_content = '\n'.join(lines)
with open('/tmp/nasr-city-ops/update_perf.py', 'w') as f:
    f.write(new_content)

print("Done patching update_perf.py")
for vc, sd in SHEET_DATA.items():
    print(f"  {vc}: fir_yday={sd['fir'][5]}, tc_yday={sd['tc'][5]}, avtc_yday={sd['avtc'][5]}")
