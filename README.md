# BESS Device Profiles [![CI](https://github.com/bess-solutions/bess-device-profiles/actions/workflows/ci.yml/badge.svg)](https://github.com/bess-solutions/bess-device-profiles/actions)

Fuente única de verdad (SSOT) de perfiles de dispositivos industriales para almacenamiento en baterías (BESS), inversores híbridos y sistemas BMS.

> **Política de Veracidad:** Los perfiles de fabricante provienen de la documentación técnica oficial y de especificaciones Modbus/SunSpec de la industria. Su nivel de verificación es `unverified` (sin prueba contra hardware físico en banco de pruebas), salvo el perfil de referencia emulado.

---

## 📂 Clasificación de Perfiles

### Tier 1: Perfiles con Bindings Canónicos (Consumibles por `open-bess-edge`)
Estos perfiles definen tanto el mapa de registros (`registers`) como el mapeo estándar (`canonical`) de telemetría física (`frequency_hz`, `v_grid_v`, `p_kw`, `q_kvar`, `soc_pct`, `soh_pct`).

| Perfil | Fabricante | Modelo | Modo Edge | Nivel |
|---|---|---|---|---|
| [`open_bess_edge_reference.json`](profiles/open_bess_edge_reference.json) | BESS Solutions | Inversor / PCS de Referencia | **Control** | Reference (Emulado) |
| [`huawei_sun2000.json`](profiles/huawei_sun2000.json) | Huawei | SUN2000-(2KTL-6KTL)-L1 | Monitor | Unverified |
| [`sma_sunny_tripower.json`](profiles/sma_sunny_tripower.json) | SMA | Sunny Tripower Storage 60 | Monitor | Unverified |
| [`fronius_gen24_byd.json`](profiles/fronius_gen24_byd.json) | Fronius | Symo GEN24 Plus + BYD | Monitor | Unverified |
| [`solaredge_storedge.json`](profiles/solaredge_storedge.json) | SolarEdge | StorEdge SE5000H / SE7K | Monitor | Unverified |
| [`victron_multiplus2.json`](profiles/victron_multiplus2.json) | Victron | MultiPlus-II GX 48/5000 | Monitor | Unverified |

### Tier 2: Diccionarios Declarativos (Pendiente de Bindings Canónicos)
Perfiles que contienen mapas de registros Modbus completos o tramas CAN bus de fabricantes, disponibles como especificación abierta pero aún sin mapeo a las variables canónicas de control del gateway:

- [`deye_sunsynk_hybrid.json`](profiles/deye_sunsynk_hybrid.json): Inversores Deye / Sunsynk trifásicos (Modbus TCP).
- [`goodwe_lynx_home.json`](profiles/goodwe_lynx_home.json): Baterías GoodWe Lynx Home (Modbus TCP).
- [`byd_battery_box.json`](profiles/byd_battery_box.json): BYD Battery-Box Premium (CAN Bus Protocol v1.03).
- [`tesla_powerwall3.json`](profiles/tesla_powerwall3.json): Tesla Powerwall 3 (CAN / REST / Neurio).

---

## 🛠️ Validación Semántica
Para auditar la sintaxis JSON, correspondencia de tipos de datos (e.g. `INT32` exige `count >= 2`) y coherencia de registros:

```bash
python validate_profiles.py
```
