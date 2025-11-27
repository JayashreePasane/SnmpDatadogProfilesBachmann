# generate_phase_metrics.py

# 0 = main, 1..19 =  link 1..link-19
units = range(0, 20) 

# 0,1,2 phases
phases = [
    (0, "L1"),
    (1, "L2"),
    (2, "L3"),
]

# metrices to collect
metrics = [
    (1,  "bacVoltage",             "gauge"),
    (2,  "bacPeakVoltage",         "gauge"),
    (4,  "bacCurrent",             "gauge"),
    (5,  "bacPeakCurrent",         "gauge"),
    (17, "bacPowerFactor",         "gauge"),
    (18, "bacApparentPower",       "gauge"),
    (19, "bacActivePower",         "gauge"),
    (20, "bacPeakActivePower",     "gauge"),
    (22, "bacReactivePower",       "gauge"),
    (32, "bacApparentEnergy",      "counter"),
    (34, "bacReactiveEnergy",      "counter"),
    (36, "bacActiveEnergy",        "counter"),
    (38, "bacActiveEnergyUser",    "counter"),
]

template = """
  - MIB: BACHMANN-BLUENET-MIB
    symbol:
      OID: 1.3.6.1.4.1.31770.2.2.8.4.1.5.{unitIndex}.0.0.{phaseIndex}.255.255.0.{metricCode}
      name: {metricName}{unitNameSuffix}{phaseName}
    metric_tags:
      - tag: unit_id
        value: "{unitId}"
      - tag: unit_name
        value: "{unitTagName}"
      - tag: phase
        value: "{phaseName}"
      - tag: measurement_level
        value: "phase"
    metric_type: {metricType}
"""

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
for unit in units:
    if unit == 0:
        unit_name_suffix = "Main"
        unit_tag_name = "main"
    else:
        unit_name_suffix = f"Link{unit}"
        unit_tag_name = f"link_{unit}"

    for phaseIndex, phaseName in phases:
        for metricCode, baseName, metricType in metrics:
            print(
                template.format(
                    unitIndex=unit,
                    phaseIndex=phaseIndex,
                    metricCode=metricCode,
                    metricName=baseName,
                    unitNameSuffix=unit_name_suffix,
                    phaseName=phaseName,
                    unitId=unit,
                    unitTagName=unit_tag_name,
                    metricType=metricType,
                )
            )
