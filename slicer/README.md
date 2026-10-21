# Machine-independent slicer profiles

Choose a profile by **toolhead, nozzle, material and print process**.
Changing from BIG-Meter to BIG-60 or BIG-180X does not create a new ULTRA material or print process.
The printer's own preset supplies its work envelope, hardware limits and calibration.

## Download and import the starter bundle

**[Hjort-Creations-Modix-BIG-PrusaSlicer.ini](https://github.com/HjortCreations/modix-big-series/releases/download/v0.3.1/Hjort-Creations-Modix-BIG-PrusaSlicer.ini)**

1. In PrusaSlicer 2.9.6, choose **File > Import > Import Config Bundle** and select the downloaded file.
2. Select your **Hjort Creations - model - head/nozzle** printer preset.
3. Select **Hjort Creations - BIG Starter - Layer 0.4** and the matching **Hjort Creations - PLA** preset.
4. Check the selected nozzle and usable build volume, set up the physical printer/upload address locally, and slice a small test.

One download imports all 15 printer presets, one shared print preset and three PLA presets.
There is no user build step. Existing differently named presets are retained.
The machine needs a working config.g/homing/bed.g and the shared stop.g and adaptive_mesh.g first;
see [macro installation and requirements](../macros/README.md). The bundle does not upload system files.
Keep an already commissioned bed.g; the optional shared U-tilt has its own four-Z-motor requirements.

| Printer model | Starter build volume X/Y/Z, mm |
|---|---|
| BIG-60 | 600 / 600 / 660 |
| BIG-120X | 1200 / 600 / 640 |
| BIG-120Z | 600 / 600 / 1200 |
| BIG-180X | 1800 / 600 / 600 |
| BIG-Meter | 980 / 1000 / 1000 |

Sources: [Modix Generation 4 specifications](https://www.modix3d.com/tech2/),
[Modix catalogue](https://www.modix3d.com/_downloads/brochures/Modix-Catalog-Filament-line.pdf)
and [current comparison](https://www.modix3d.com/tech-specs/), checked 2026-10-21.
BIG-180X deliberately retains the conservative 600 mm Z value: the current comparison also lists 660 mm.
BIG-Meter dimensions use the existing official V4 reference; some older/upgraded machines have less travel.
Always match the local preset to actual reachable travel. Catalogue size does not establish wiring or probe reach.
Everest's verified 970 / 1030 / 2000 mm dimensions are recorded but excluded: PrusaSlicer 2.9.6
[limits max_print_height to 1200 mm](https://github.com/prusa3d/PrusaSlicer/blob/version_2.9.6/src/libslic3r/PrintConfig.cpp).
These are single-tool Cartesian RRF starting presets, not IDEX or complete GEN5 firmware configurations.

| PLA preset | Default nozzle, mm | Max flow, mm³/s | First / normal temperature, °C | Starting PA |
|---|---|---|---|---|
| Griffin | 0.8 | 30 | 235 / 225 | 0.015 |
| Griffin High-Flow | 0.8 | 40 | 235 / 225 | 0.015 |
| Griffin ULTRA | 1.4 | 80 | 235 / 215 | 0.035 |

These are generic PLA starting values for tuning, not measured limits for every nozzle/material.
High-Flow's conservative 40 mm³/s cap was requested by the operator; 60 is deliberately not used for High-Flow.
ULTRA 1.4 starts at the operator's conservative 80 mm³/s value; the separate 1.8 mm profile retains the operator's 100 mm³/s working setting.
All three target 45 s minimum layer time, 5 mm/s minimum print speed, no fan for the first two layers
and full fan at layer 5. The speed floor can prevent achieving 45 s on very small layers; inspect cooling in preview.
PLA temperatures, extrusion multiplier, PA and flow are intended to be tuned to the installed head/nozzle/material.

The shared process uses automatic widths (all width fields zero), 0.4 mm layers/first layer, two walls,
15% adaptive cubic infill and the existing shared start/end sequence. Infill combination is disabled for this baseline.
Print/travel acceleration stays 250/800; feature acceleration overrides stay zero.
Axis speed limits remain in the printer firmware. Slicer machine limits are used only for time estimation.
The selected PLA preset supplies PA in its filament start G-code, after the shared printer startup.
Build-plate heat is disabled. Filament dependencies match head identifiers in printer notes, never a customer or model name.
They filter/mark compatibility rather than provide a hard lock. Later layer-height presets can also match nozzle diameter.
Min/max layer heights are prepared in the nozzle presets; changing the diameter manually does not recalculate them.

## Independent presets for existing printer setups

| Profile package | Toolhead / nozzle | Process | Material |
|---|---|---|---|
| profile-griffin-0.6-pla | Griffin 0.6 mm | 0.2 mm layers | PLA |
| profile-griffin-0.8-addnorth-epla | Griffin 0.8 mm | 0.4 mm layers | addnorth ePLA |
| profile-ultra-1.8-formfutura-epla | Griffin ULTRA 1.8 mm | 1.0 mm layers | FormFutura ePLA |

Download the matching profile ZIP from
[Releases](https://github.com/HjortCreations/modix-big-series/releases).
These ZIPs do not contain firmware, homing files, model geometry or a replacement printer preset.

## Use with an existing printer preset

1. Import PrusaSlicer-process-material.ini with **File → Import → Import Config Bundle**.
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
- starter.json: the single download's head/material choices; machines.json: sourced slicer work envelopes only.

The starter reuses existing components through explicit base inheritance. Adding a model adds only its dimensions;
it does not copy print/material settings or generate unverified homing, motor mappings or M671 screw geometry.
Maintainers build the ready-made file with python tools/build.py --starter; users only download and import it.

The current ULTRA 1.8 mm/ePLA baseline uses 100 mm³/s, 235/215 °C, PA 0.035 and print/travel acceleration 250/800 mm/s².
Those are shared working defaults for that setup across sizes, not a measured maximum for every material or nozzle.

Prepared combinations that also contain a particular printer's geometry remain available as **example-** packages.
They are convenience examples, not the compatibility list for these reusable profiles or the shared macros.

The G32 call uses the printer's configured bed.g. The shared U-tilt option needs four independent Z motors; other mechanisms retain their own compatible alignment routine. Adaptive mesh is independent of that choice.
