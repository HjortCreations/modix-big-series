# Modix BIG Series

Shared RepRapFirmware macros and PrusaSlicer profiles for the Modix BIG series.
**Griffin and Griffin ULTRA toolheads are independent of machine size.**

## Download and use

Download a prebuilt ZIP package from [Releases](https://github.com/HjortCreations/modix-big-series/releases).
Read the [installation guide](docs/installation.md) before copying system files to a printer.
Packages extend an existing, working Modix configuration; they do not replace `config.g`.

| Package | Work envelope, mm | Toolhead / nozzle | Material / process |
|---|---|---|---|
| `big-120z-griffin-0.6` | BIG-120Z V4, 600 × 600 × 1200 | Griffin 0.6 mm | PLA, 0.2 mm layers |
| `big-meter-griffin-0.8` | BIG-Meter V4 reference, 980 × 1000 × 1000 | Griffin 0.8 mm | addnorth ePLA, 0.4 mm layers |
| `big-meter-ultra-1.8` | BIG-Meter upgraded legacy variant, 965 × 980 × 1000 | ULTRA 1.8 mm | FormFutura ePLA, 1.0 mm layers |

These are established work envelopes, not guaranteed dimensions for every machine of the same model.
The sources have been migrated and checked offline. **The newly assembled packages have not yet been installed or physically tested.**
More BIG sizes can be added once their geometry and hardware have been verified. IDEX and other Z-drive arrangements are not currently supported.

## Where settings belong

| Component | Responsibility |
|---|---|
| `firmware/common/` | One U-tilt routine, one stop.g, adaptive mesh and axis test |
| `config/models/` | Work envelope and Z-screw geometry |
| `config/hardware/`, `firmware/hardware/` | Controller, endstop directions and existing homing routines |
| `config/motion/`, `config/motors/` | Motion limits, time estimates and optional motor parameters |
| `config/toolheads/` | Toolhead clearance; no universal BLTouch offset |
| `slicer/toolheads/` | Nozzle size, retraction and layer-height limits |
| `slicer/processes/` | Layers, walls, infill, speeds and print acceleration |
| `slicer/materials/` | Temperature, cooling, flow and pressure advance for a material/toolhead/nozzle combination |
| `slicer/gcode/` | Shared start, end and layer-change G-code |
| `recipes/` | Small files that select a combination of components |

The same ULTRA process and material components can be reused on another model without copying them.
The [example recipe](examples/big-120z-ultra-1.8.json) demonstrates this composition; it is not a commissioned machine profile.

## Shared behaviour

- Heat the nozzle during homing. Home all axes if Z is unknown; otherwise home XY only.
- Run conditional G32: reuse successful bed alignment while Z remains held and the toolhead is unchanged. `G32 S1` forces realignment.
- Probe an adaptive mesh for each print. The U-shaped tilt path reverses between passes.
- Retain the Modix end sequence through M0 → stop.g: retract while hot, turn off tool heating, lower the bed towards at least Z300 without exceeding Z-max, park at X1 Y1 and retain Z holding current.
- Set acceleration, axis speed limits and pressure advance in start G-code. Slicer acceleration overrides remain zero.
- Leave bed heating disabled and use the same descriptive output filename format throughout.

ULTRA 1.8 mm working settings: **100 mm³/s, 235/215 °C, PA 0.035, print/travel acceleration 250/800 mm/s²**,
1.0 mm layers, a 1.2 mm first layer and 1.2 mm retraction at 35 mm/s. These are operator-reported working settings, not a measured maximum throughput.
G-code resolution remains **0.0125 mm** in the migrated baseline; the proposed 0.05 mm setting has not been applied automatically.

## Build and check

Requires Python 3.10+ with no additional Python packages.

```console
python tools/check.py
python tools/build.py --all
```

Output goes into the ignored dist/ directory. Each ZIP contains a manifest, system files and two slicer formats:
PrusaSlicer.ini for **Import Config**, and PrusaSlicer-bundle.ini for **Import Config Bundle**.
The bundle uses the same process and material preset names across machine sizes.

[Maintenance rules](AGENTS.md) · [Components and changes](docs/maintenance.md) · [Validation status](docs/validation.md)
