# generate_outlet_state_profile.py

SNMP_PREFIX = "1.3.6.1.4.1.31770.2.2.9.1.1.5"

# 0 = Main, 1..19 = Link PDUs
UNITS = range(0, 20)
OUTLETS = range(0, 12)

PHASES = {
    0: "L1",
    1: "L2",
    2: "L3",
}

def get_phase_for_outlet(outlet_index: int) -> int:
    """Outlet 0–3 → L1, 4–7 → L2, 8–11 → L3"""
    return outlet_index // 4  # 0, 1, 2


print("sysobjectid: 1.3.6.1.4.1.31770.*\n")
print("metadata:")
print("  device:")
print("    vendor: \"bachmann\"")
print("    type: \"pdu\"\n")
print("metrics:")

for unit in UNITS:
    unit_name = "main" if unit == 0 else f"link_{unit}"
    unit_suffix = "Main" if unit == 0 else f"Link{unit}"

    for outlet in OUTLETS:
        phase_idx = get_phase_for_outlet(outlet)
        phase_name = PHASES[phase_idx]
        
        # 1.3.6.1.4.1.31770.2.2.9.1.1.5.<unit>.0.0.<phase_idx>.0.<outlet>.0.0
        oid = f"{SNMP_PREFIX}.{unit}.{0}.{0}.{phase_idx}.{0}.{outlet}.{0}.{0}"

        metric_name = f"bacSocketStatus{unit_suffix}{phase_name}Outlet{outlet+1}"

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
        print("      - tag: outlet")
        print(f"        value: \"{outlet+1}\"")
        print("      - tag: measurement_level")
        print("        value: \"outlet\"")
        print("    metric_type: gauge\n")
