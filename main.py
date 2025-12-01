import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

GENERATORS = [
    ("generate_inlet_profile.py",       "bachmann_inlet_metrics.yaml"),
    ("generate_phase_profile.py",        "bachmann_phase_metrics.yaml"),
    ("generate_outlet_per_phase_profile.py",    "bachmann_outlet_metrics.yaml"),
    ("generate_io_profile_metrics.py",     "bachmann_io_metrics.yaml"),
    ("generate_sensor_profile.py",     "bachmann_sensors_metrics.yaml"),
    ("generate_phase_status_profile.py",     "bachmann_phase_status.yaml"),
    ("generate_outlet_status_profile.py",     "bachmann_outlet_status.yaml"),
    ("generate_inlet_status_profile.py",     "bachmann_inlet_status.yaml"),
    ("generate_global_status_profile.py",     "bachmann_global_status.yaml"),
]

def run_generator(script_name: str, output_name: str) -> None:
    script_path = BASE_DIR / script_name
    output_path = BASE_DIR / output_name

    if not script_path.is_file():
        print(f"[ERROR] Generator script not found: {script_path}", file=sys.stderr)
        return

    print(f"[INFO] Generating {output_name} using {script_name} ...")

    with output_path.open("w", encoding="utf-8") as f:
        subprocess.run(
            [sys.executable, str(script_path)],
            stdout=f,
            stderr=subprocess.PIPE,
            check=True,
        )

    print(f"[OK]  Wrote {output_name}")


def write_parent_profile() -> None:
    parent_path = BASE_DIR / "bachmann_pdu.yaml"
    print(f"[INFO] Writing parent profile: {parent_path.name}")

    content = """extends:
  - bachmann_inlet_metrics
  - bachmann_phase_metrics
  - bachmann_outlet_metrics
  - bachmann_io_metrics
  - bachmann_sensors_metrics
  - bachmann_phase_status
  - bachmann_outlet_status
  - bachmann_inlet_status
  - bachmann_global_status

sysobjectid: 1.3.6.1.4.1.31770.*

metadata:
  device:
    vendor: "bachmann"
    type: "pdu"
"""

    parent_path.write_text(content, encoding="utf-8")
    print(f"[OK]  Wrote {parent_path.name}")


def main() -> None:
    # 1) Run all generators to create individual profiles
    for script, output in GENERATORS:
        run_generator(script, output)

    # 2) Create parent profile that includes all 3
    write_parent_profile()

    print("\n[DONE] All profiles generated:")
    print("  - bachmann_inlet_metrics.yaml")
    print("  - bachmann_phase_metrics.yaml")
    print("  - bachmann_outlet_metrics.yaml")
    print("  - bachmann_io_metrics.yaml")
    print("  - bachmann_sensors_metrics.yaml")
    print("  - bachmann_phase_status.yaml")
    print("  - bachmann_outlet_status.yaml")
    print("  - bachmann_inlet_status.yaml")
    print("  - bachmann_global_status.yaml")
    print("  - bachmann_pdu.yaml (parent profile)")


if __name__ == "__main__":
    main()
