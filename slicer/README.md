# Machine-independent slicer profiles

Choose a profile by **toolhead, nozzle, material and print process**.
Changing from BIG-Meter to BIG-60 or BIG-180X does not create a new ULTRA material or print process.
The printer's own preset supplies its work envelope, hardware limits and calibration.

| Profile package | Toolhead / nozzle | Process | Material |
|---|---|---|---|
| profile-griffin-0.6-pla | Griffin 0.6 mm | 0.2 mm layers | PLA |
| profile-griffin-0.8-addnorth-epla | Griffin 0.8 mm | 0.4 mm layers | addnorth ePLA |
| profile-ultra-1.8-formfutura-epla | Griffin ULTRA 1.8 mm | 1.0 mm layers | FormFutura ePLA |

Download the matching profile ZIP from
[Releases](https://github.com/HjortCreations/modix-big-series/releases).
These ZIPs do not contain firmware, homing files, model geometry or a replacement printer preset.

## Use with an existing printer preset

1. Import PrusaSlicer-process-material.ini with **File â†’ Import â†’ Import Config Bundle**.
   This imports Print Settings and Filament Settings only. Select them alongside your existing printer preset.
2. Check that the existing printer preset matches the chosen nozzle and head settings.
   toolhead-settings-reference.json lists the shared nozzle, retraction and extrusion-mode settings without any machine geometry.
3. Use the supplied gcode/start.gcode, gcode/end.gcode and gcode/before-layer.gcode in the printer preset's corresponding custom G-code fields.
   Start and layer snippets contain PrusaSlicer placeholders; paste them into the slicer, not the printer console.
4. Install the shared macros referenced by the start/end sequence separately. They are available as independent features.
5. Keep the machine's own axis speed limits. The independent head profile does not set M203.

Older combination examples retain their known M203 overrides in the printer preset's start code.
When switching to the independent head profile, keep the desired commissioned speed limits in the machine configuration instead; this build does not change them on the printer.

The same process/material preset names are used across machine sizes. No model recipe is required to build these profiles:

```console
python tools/build.py --profiles
```

## Settings ownership

- toolheads/: nozzle diameter, retraction and layer-height limits.
- processes/: layers, walls, infill, print speeds and default print acceleration.
- materials/: temperature, cooling, flow limit and pressure advance for the selected material/nozzle/head.
- common/startup.json: common default travel acceleration.
- gcode/: the shared start/end/layer-change sequence.

The current ULTRA 1.8 mm/ePLA baseline uses 100 mmÂ³/s, 235/215 Â°C, PA 0.035 and print/travel acceleration 250/800 mm/sÂ².
Those are shared working defaults for that setup across sizes, not a measured maximum for every material or nozzle.

Prepared combinations that also contain a particular printer's geometry remain available as **example-** packages.
They are convenience examples, not the compatibility list for these reusable profiles or the shared macros.

The G32 call uses the printer's configured bed.g. The shared U-tilt option needs four independent Z motors; other mechanisms retain their own compatible alignment routine. Adaptive mesh is independent of that choice.
