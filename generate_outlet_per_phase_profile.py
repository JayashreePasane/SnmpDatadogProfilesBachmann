# generate_outlet_per_phase_profile.py

# Units: 0 = main, 1..19 = link PDUs
UNIT_IDS = range(0, 20)

# 3 phases per PDU
PHASES = [
    (0, "L1"),  # phase index 0 
    (1, "L2"),  # phase index 1 
    (2, "L3"),  # phase index 2 
]

# 4 outlets per phase on each PDU (0..3) - check EZB configuration 
OUTLETS_PER_PHASE = 4

METRICS = [
    (4,   "bacCurrent",               "gauge"),
    (5,   "bacPeakCurrent",           "gauge"),
    (17,  "bacPowerFactor",           "gauge"),
    (18,  "bacApparentPower",         "gauge"),
    (19,  "bacActivePower",           "gauge"),
    (20,  "bacPeakActivePower",       "gauge"),
    (22,  "bacReactivePower",         "gauge"),
    (32,  "bacApparentEnergy",        "counter"),
    (34,  "bacReactiveEnergy",        "counter"),
    (36,  "bacActiveEnergy",          "counter"),
    (38,  "bacActiveEnergyUser",      "counter"),
]

#bluenetGen2VariableDataTable OID
SNMP_PREFIX = "1.3.6.1.4.1.31770.2.2.8.4.1.5"


def build_obis_phase_outlet(phase_idx, outlet_idx, metric_code):
    """
    Build OBIS tuple for per-phase per-outlet metrics:

      phase 0 (L1): 0.0.0.0.0.(0+outlet).0.metric
      phase 1 (L2): 0.0.0.1.0.(4+outlet).0.metric
      phase 2 (L3): 0.0.0.2.0.(8+outlet).0.metric

    which is equivalent to:

      dlms_phase = phase_idx + 1          # 0,1,2
      out_code   = phase_idx*4 + outlet   # 0..3, 4..7, 8..11
    """
    dlms_phase = phase_idx              
    out_code = phase_idx * 4 + outlet_idx    
    return [0, 0, 0, dlms_phase, 0, out_code, 0, metric_code]


def snmp_oid_for_unit_and_obis(unit_id, obis):
    # obis = [0, 0, 0, phase, 0, out_code, 0, metric]
    indices = [unit_id] + obis[1:]
    return SNMP_PREFIX + "." + ".".join(str(x) for x in indices)


def unit_name(unit_id):
    if unit_id == 0:
        return "main"
    return f"link_{unit_id}"


def unit_suffix(unit_id):
    if unit_id == 0:
        return "Main"
    return f"Link{unit_id}"


# ---- Datadog profile header ----
print("sysobjectid: 1.3.6.1.4.1.31770.*")
print("")
print("metadata:")
print("  device:")
print("    vendor: \"bachmann\"")
print("    type: \"pdu\"")
print("")
print("metrics:")

# ---- Metrics ----
for unit_id in UNIT_IDS:
    for phase_idx, phase_name in PHASES:
        for outlet in range(OUTLETS_PER_PHASE):
            for metric_code, metric_base_name, metric_type in METRICS:
                obis = build_obis_phase_outlet(phase_idx, outlet, metric_code)
                oid = snmp_oid_for_unit_and_obis(unit_id, obis)

                name = f"{metric_base_name}{unit_suffix(unit_id)}{phase_name}Outlet{outlet+1+(phase_idx*4)}"

                print("  - MIB: BACHMANN-BLUENET-MIB")
                print("    symbol:")
                print(f"      OID: {oid}")
                print(f"      name: {name}")
                print("    metric_tags:")
                print("      - tag: unit_id")
                print(f"        value: \"{unit_id}\"")
                print("      - tag: unit_name")
                print(f"        value: \"{unit_name(unit_id)}\"")
                print("      - tag: phase")
                print(f"        value: \"{phase_name}\"")
                print("      - tag: outlet")
                print(f"        value: \"{outlet+1+(phase_idx*4)}\"")
                print("      - tag: measurement_level")
                print("        value: \"outlet\"")
                print(f"    metric_type: {metric_type}\n")
