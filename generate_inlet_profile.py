# generate_inlet_profile_metrics.py

units = range(0, 20)  # 0 = main, 1..19 are link PDUs

metrics = [
    ("4",  "bacCurrent",               "gauge"),
    ("5",  "bacPeakCurrent",           "gauge"),
    ("9",  "bacNeutralCurrent",        "gauge"),
    ("18", "bacApparentPower",         "gauge"),
    ("19", "bacActivePower",           "gauge"),
    ("20", "bacPeakActivePower",       "gauge"),
    ("22", "bacReactivePower",         "gauge"),
    ("23", "bacFrequency",             "gauge"),
    ("24", "bacPeakNeutralCurrent",    "gauge"),
    ("32", "bacApparentEnergy",        "counter"),
    ("34", "bacReactiveEnergy",        "counter"),
    ("36", "bacActiveEnergy",          "counter"),
    ("38", "bacActiveEnergyUser",      "counter"),
]

# ---- Header for Datadog profile ----
print("sysobjectid: 1.3.6.1.4.1.31770.*")
print("")
print("metadata:")
print("  device:")
print("    vendor: \"bachmann\"")
print("    type: \"pdu\"")
print("")
print("metrics:")

# ---- Metrics ----
for unit in units:

    # Proper name suffix and unit_name handling
    if unit == 0:
        unit_name_suffix = "Main"
        unit_tag_name = "main"
    else:
        unit_name_suffix = f"Link{unit}"
        unit_tag_name = f"link_{unit}"

    for oid, base_name, metric_type in metrics:
        metric_name = f"{base_name}{unit_name_suffix}"

        print("  - MIB: BACHMANN-BLUENET-MIB")
        print("    symbol:")
        print(f"      OID: 1.3.6.1.4.1.31770.2.2.8.4.1.5.{unit}.0.0.255.255.255.0.{oid}")
        print(f"      name: {metric_name}")
        print("    metric_tags:")
        print("      - tag: unit_id")
        print(f"        value: \"{unit}\"")
        print("      - tag: unit_name")
        print(f"        value: \"{unit_tag_name}\"")
        print("      - tag: measurement_level")
        print("        value: \"inlet\"")
        print(f"    metric_type: {metric_type}")
        print("")
