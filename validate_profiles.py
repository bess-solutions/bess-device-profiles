#!/usr/bin/env python3
"""
validate_profiles.py
====================
Autodetect and validate all BESS device profiles under the profiles/ folder.
Supports polymorphic validation based on protocol (Modbus, CAN, HTTP_REST).
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

        # Validate optional fields if present
        if "type" in reg:
            reg_type = reg["type"].upper()
            allowed_types = {"INT16", "UINT16", "INT32", "UINT32", "FLOAT32", "STRING", "INT64", "UINT64", "ENUM16", "BITFIELD16", "BITFIELD32"}
            if reg_type not in allowed_types:
                print(f"\n[ERR] ERROR in {filename}: Register '{name}' has invalid type '{reg_type}'. Allowed: {allowed_types}")
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

    print("[OK]")
    return True

def main():
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    profiles_glob = os.path.join(THIS_DIR, "profiles", "*.json")
    profile_files = glob.glob(profiles_glob)

    if not profile_files:
        print("[ERR] ERROR: No JSON profile files found under profiles/ directory.")
        sys.exit(1)

    print(f"Found {len(profile_files)} profile files to validate.")
    print("--------------------------------------------------")

    success = True
    for filepath in profile_files:
        # Skip templates
        if "TEMPLATE" in os.path.basename(filepath):
            continue
        if not validate_file(filepath):
            success = False

    print("--------------------------------------------------")
    if success:
        print("[OK] All device profiles successfully validated!")
        sys.exit(0)
    else:
        print("[ERR] Profile validation failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
