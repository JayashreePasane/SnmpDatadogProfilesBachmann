# generate_sensor_profile.py
#
# sensors: temperature + humidity
# OBIS pattern:
#   0.1.0.<idx>.255.2.1.0 -> temperature
#   0.1.0.<idx>.255.2.1.1 -> humidity
#
# Main = unit 0, Links = units 1..19
# Up to 10 sensors: OBIS indices 4..13

UNIT_IDS = range(0, 20)   
SENSOR_INDEXES = range(4, 14) 

METRICS = [
    (0, "bacTemperature", "gauge"),
    (1, "bacHumidity",    "gauge"),
]

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
    OBIS: [0, 1, 0, idx, 255, 2, 1, metric_code]
    SNMP index: <unit_id>.1.0.<idx>.255.2.1.<metric_code>
    (drop first 0, prepend unit_id)
    """
    indices = [unit_id] + obis[1:]
    return SNMP_PREFIX + "." + ".".join(str(x) for x in indices)


for unit_id in UNIT_IDS:
    for sensor_idx in SENSOR_INDEXES:
        for metric_code, base_name, metric_type in METRICS:
            # OBIS: 0.1.0.<sensor_idx>.255.2.1.<metric_code>
            obis = [0, 1, 0, sensor_idx, 255, 2, 1, metric_code]
            oid = snmp_oid_for_unit_and_obis(unit_id, obis)

            # keep sensor index in name so each sensor is unique
            metric_name = f"{base_name}{unit_suffix(unit_id)}Sensor{sensor_idx-4}"
            sensor_index_str = str(sensor_idx-4)

            print("  - MIB: BACHMANN-BLUENET-MIB")
            print("    symbol:")
            print(f"      OID: {oid}")
            print(f"      name: {metric_name}")
            print("    metric_tags:")
            print("      - tag: unit_id")
            print(f"        value: \"{unit_id}\"")
            print("      - tag: unit_name")
            print(f"        value: \"{unit_name(unit_id)}\"")
            print("      - tag: sensor_index")
            print(f"        value: \"{sensor_index_str}\"")
            print("      - tag: measurement_level")
            print("        value: \"external_sensor\"")
            print(f"    metric_type: {metric_type}")
            print("")

