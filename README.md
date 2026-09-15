# BESS Solutions — Device Profiles

This repository centralizes industrial hardware device profiles used by **BESS Solutions** and the **Open BESS Edge** (`open-bess-edge`). It defines holding register mappings, scales, and byte orders for power conversion systems (PCS), battery management systems (BMS), and smart meters.

Separating these configurations from the main gateway logic allows:
- **Rapid hardware onboarding:** Add support for new inverters by writing a single JSON file without altering code.
- **Independent versioning:** Device updates do not require rebuilding or redeploying the core edge gateway.
- **Easy contribution:** Open to manufacturers (BYD, Tesla, Huawei, SMA, etc.) and developers to maintain accurate register configurations.

---

## 📂 Profiles Folder

All device profiles live under the `profiles/` directory:
- `huawei_sun2000.json` - Huawei SUN2000 Inverter Series.
- `sma_sunny_tripower.json` - SMA Sunny Tripower Inverter.
- `victron_multiplus2.json` - Victron Multiplus II PCS.
- `fronius_gen24_byd.json` - Fronius Gen24 Hybrid + BYD Combo.
- `byd_battery_box.json` - BYD Battery Box BMS.
- `tesla_powerwall3.json` - Tesla Powerwall 3 BMS/Inverter.
- `solaredge_storedge.json` - SolarEdge StorEdge.

---

## ⚙️ Profile Schema Structure

Each JSON profile conforms to the following schema:

```json
{
  "name": "Device Model Name",
  "manufacturer": "Manufacturer Name",
  "connection": {
    "type": "modbus_tcp",
    "default_port": 502,
    "byte_order": "BIG",
    "word_order": "BIG"
  },
  "registers": [
    {
      "address": 32080,
      "tag": "ActivePower",
      "type": "int32",
      "scale": 1.0,
      "permission": "r",
      "description": "Active Power Output in Watts"
    }
  ]
}
```

### Fields:
*   `byte_order` / `word_order`: Registers byte ordering (`BIG` or `LITTLE` endianness).
*   `address`: Modbus 0-based holding register address.
*   `tag`: Unique string identifier used by the gateway logic and metrics endpoints.
*   `type`: Data format (e.g. `int16`, `uint16`, `int32`, `uint32`, `float32`).
*   `scale`: Multiplication factor to convert raw register values to real units (e.g., `0.1` for temperature/SoC, `1.0` for Watts).
*   `permission`: Access control (`r` for Read-only, `w` for Write-only, `rw` for Read-Write).

---

## 🤝 How to Contribute

Adding support for a new inverter or meter is the perfect way to get started with the BESS Solutions ecosystem:

1.  **Fork** this repository.
2.  Create a new JSON file under `profiles/` matching the format of `TEMPLATE_interop_certification.json`.
3.  Add the Modbus addresses matching your manufacturer's datasheet.
4.  Submit a **Pull Request**.

All submissions are automatically validated by our CI schema checker.

---
*BESS Solutions SpA — open@bess-solutions.cl*
