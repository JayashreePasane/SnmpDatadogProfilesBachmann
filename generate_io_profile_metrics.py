# generate_io_profile_metrics.py
#
# Generates a Datadog SNMP profile (bachmann_io.yml) for IO/electrical channels
# Main = unit 0, Links = units 1..19

UNIT_IDS = range(0, 20)  # 0 = main, 1..19 = link PDUs

# channels: (obis_index, metric_code, base_name)
# OBIS: 0.1.0.<index>.255.16.1.<code>
CHANNELS = [
    (0, 6, "ioOutputChannel1"),
    (1, 7, "ioOutputChannel2"),
    (2, 4, "ioInputChannel3"),
    (3, 5, "ioInputChannel4"),
]

# SNMP base OID prefix
SNMP_PREFIX = "1.3.6.1.4.1.31770.2.2.8.4.1.5"

# ---- Datadog profile header ----
print("sysobjectid: 1.3.6.1.4.1.31770.*")
print("")
print("metadata:")
print("  device:")
print("    vendor: \"bachmann\"")
print("    type: \"pdu\"")
print("")
print("metrics:")


def unit_name(unit_id: int) -> str:
    return "main" if unit_id == 0 else f"link_{unit_id}"


def unit_suffix(unit_id: int) -> str:
    return "Main" if unit_id == 0 else f"Link{unit_id}"


def snmp_oid_for_unit_and_obis(unit_id: int, obis: list[int]) -> str:
    """
    Map OBIS [0,1,0,<idx>,255,16,1,<code>] into SNMP OID:

      SNMP_PREFIX.<unit_id>.1.0.<idx>.255.16.1.<code>
    """
    indices = [unit_id] + obis[1:]
    return SNMP_PREFIX + "." + ".".join(str(x) for x in indices)


for unit_id in UNIT_IDS:
    for obis_index, metric_code, base_name in CHANNELS:
        # OBIS: 0.1.0.<index>.255.16.1.<metric_code>
        obis = [0, 1, 0, obis_index, 255, 16, 1, metric_code]
        oid = snmp_oid_for_unit_and_obis(unit_id, obis)

        metric_type = "gauge"  
        metric_name = f"{base_name}{unit_suffix(unit_id)}"

        print("  - MIB: BACHMANN-BLUENET-MIB")
        print("    symbol:")
        print(f"      OID: {oid}")
        print(f"      name: {metric_name}")
        print("    metric_tags:")
        print("      - tag: unit_id")
        print(f"        value: \"{unit_id}\"")
        print("      - tag: unit_name")
        print(f"        value: \"{unit_name(unit_id)}\"")
        print("      - tag: channel")
        print(f"        value: \"{base_name}\"")
        print("      - tag: measurement_level")
        print("        value: \"io\"") 
        print(f"    metric_type: {metric_type}")
        print("")

