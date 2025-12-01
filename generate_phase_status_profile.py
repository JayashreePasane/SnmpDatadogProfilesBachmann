# generate_phase_status_profile.py

SNMP_PREFIX = "1.3.6.1.4.1.31770.2.2.9.1.1.5"

# 0 = Main, 1..19 = Link PDUs
UNITS = range(0, 20)

PHASES = {
    0: "L1",
    1: "L2",
    2: "L3",
}

print("sysobjectid: 1.3.6.1.4.1.31770.*\n")
print("metadata:")
print("  device:")
print("    vendor: \"bachmann\"")
print("    type: \"pdu\"\n")
print("metrics:")

for unit in UNITS:
    # naming consistent with your other profiles
    unit_name = "main" if unit == 0 else f"link_{unit}"
    unit_suffix = "Main" if unit == 0 else f"Link{unit}"

    for phase_idx, phase_name in PHASES.items():
        # 1.3.6.1.4.1.31770.2.2.9.1.1.5.<unit>.0.0.<phase_idx>.255.255.0.0
        oid = f"{SNMP_PREFIX}.{unit}.0.0.{phase_idx}.255.255.0.0"

        metric_name = f"bacPhaseStatus{unit_suffix}{phase_name}"

        print("  - MIB: BACHMANN-BLUENETGEN2-MIB")
        print("    symbol:")
        print(f"      OID: {oid}")
        print(f"      name: {metric_name}")
        print("    metric_tags:")
        print("      - tag: unit_id")
        print(f"        value: \"{unit}\"")
        print("      - tag: unit_name")
        print(f"        value: \"{unit_name}\"")
        print("      - tag: phase")
        print(f"        value: \"{phase_name}\"")
        print("      - tag: measurement_level")
        print("        value: \"phase\"")
        print("    metric_type: gauge\n")
