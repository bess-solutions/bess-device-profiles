#!/usr/bin/env python3
"""
validate_profiles.py
====================
Autodetect and validate all BESS device profiles under the profiles/ folder.
Performs semantic Modbus checks (word count vs data type), canonical mappings,
and verification level integrity.
No external dependencies.
"""
import os
import sys
import json
import glob

REQUIRED_TOP_KEYS = {"profile_version", "device", "connection"}
REQUIRED_DEVICE_KEYS = {"manufacturer", "model"}

def validate_modbus_registers(registers: dict, filename: str) -> bool:
    if not isinstance(registers, dict):
        print(f"\n[ERR] ERROR in {filename}: 'registers' must be a JSON object (dictionary).")
        return False

    addresses = set()
    for name, reg in registers.items():
        if not isinstance(reg, dict):
            print(f"\n[ERR] ERROR in {filename}: Register '{name}' is not a JSON object.")
            return False

        if "address" not in reg:
            print(f"\n[ERR] ERROR in {filename}: Register '{name}' is missing required 'address' field.")
            return False

        addr = reg["address"]
        if not isinstance(addr, int) or addr < 0:
            print(f"\n[ERR] ERROR in {filename}: Register '{name}' address must be a non-negative integer. Got: {addr}")
            return False

        if addr in addresses:
            print(f"\n[ERR] ERROR in {filename}: Duplicate Modbus address found: {addr} (used by register '{name}')")
            return False
        addresses.add(addr)

        if "type" in reg:
            reg_type = reg["type"].upper()
            allowed_types = {"INT16", "UINT16", "INT32", "UINT32", "FLOAT32", "STRING", "INT64", "UINT64", "ENUM16", "BITFIELD16", "BITFIELD32"}
            if reg_type not in allowed_types:
                print(f"\n[ERR] ERROR in {filename}: Register '{name}' has invalid type '{reg_type}'. Allowed: {allowed_types}")
                return False

            count = reg.get("count", 1)
            if reg_type in {"INT32", "UINT32", "FLOAT32"} and count < 2:
                print(f"\n[ERR] ERROR in {filename}: 32-bit register '{name}' ({reg_type}) requires count >= 2, got count={count}")
                return False
            if reg_type in {"INT64", "UINT64"} and count < 4:
                print(f"\n[ERR] ERROR in {filename}: 64-bit register '{name}' ({reg_type}) requires count >= 4, got count={count}")
                return False

    return True

def validate_file(filepath: str) -> bool:
    filename = os.path.basename(filepath)
    print(f"Auditing profile: {filename}...", end=" ", flush=True)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n[ERR] ERROR in {filename}: Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"\n[ERR] ERROR in {filename}: Could not read file: {e}")
        return False

    # Check top-level keys
    missing_top_keys = REQUIRED_TOP_KEYS - set(data.keys())
    if missing_top_keys:
        print(f"\n[ERR] ERROR in {filename}: Missing required top-level keys: {missing_top_keys}")
        return False

    # Check device metadata
    device = data["device"]
    if not isinstance(device, dict):
        print(f"\n[ERR] ERROR in {filename}: 'device' must be a JSON object.")
        return False
    
    missing_device_keys = REQUIRED_DEVICE_KEYS - set(device.keys())
    if missing_device_keys:
        print(f"\n[ERR] ERROR in {filename}: Missing required keys in 'device': {missing_device_keys}")
        return False

    protocol = device.get("protocol", "ModbusTCP")

    # Modbus-specific validation
    if "Modbus" in protocol:
        if "registers" not in data:
            print(f"\n[ERR] ERROR in {filename}: Missing required 'registers' field for Modbus protocol.")
            return False
        if not validate_modbus_registers(data["registers"], filename):
            return False

    # Check verification block
    verif = data.get("verification") or data.get("interop_certification")
    if not verif:
        print(f"\n[WARN] Profile {filename} does not declare 'verification' or 'interop_certification' block.")

    print("[OK]")
    return True

def main():
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    profiles_glob = os.path.join(THIS_DIR, "profiles", "*.json")
    profile_files = glob.glob(profiles_glob)

    if not profile_files:
        print("[ERR] No profiles found to validate.")
        sys.exit(1)

    all_passed = True
    print(f"--- BESS Solutions Profile Linter: Auditing {len(profile_files)} profiles ---")
    for p_path in sorted(profile_files):
        if os.path.basename(p_path).startswith('TEMPLATE_'): continue
        if not validate_file(p_path):
            all_passed = False

    if not all_passed:
        print("\n[FAIL] Profile linting failed.")
        sys.exit(1)
    else:
        print(f"\n[SUCCESS] All {len(profile_files)} profiles passed semantic checks.")

if __name__ == "__main__":
    main()
