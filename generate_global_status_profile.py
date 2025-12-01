# generate_global_status_profile.py

SNMP_PREFIX = "1.3.6.1.4.1.31770.2.2.9.1.1.5"

# 0 = Main, 1..19 = Link PDUs
UNITS = range(0, 20)

print("sysobjectid: 1.3.6.1.4.1.31770.*\n")
print("metadata:")
print("  device:")
print("    vendor: \"bachmann\"")
print("    type: \"pdu\"\n")
print("metrics:")

    
# 1.3.6.1.4.1.31770.2.2.9.1.1.5.255.0.255.255.255.255.0.0
oid = f"{SNMP_PREFIX}.{255}.{0}.{255}.{255}.{255}.{255}.{0}.{0}"

metric_name = f"bacGlobalStatus"

print("  - MIB: BACHMANN-BLUENETGEN2-MIB")
print("    symbol:")
print(f"      OID: {oid}")
print(f"      name: {metric_name}")
print("    metric_tags:")
print("      - tag: measurement_level")
print("        value: \"global\"")
print("    metric_type: gauge\n")
