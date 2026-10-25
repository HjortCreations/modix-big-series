# Machine-independent slicer profiles

Choose a profile by **toolhead, nozzle, material and print process**.
Changing from BIG-Meter to BIG-60 or BIG-180X does not create a new ULTRA material or print process.
The printer's own preset supplies its work envelope, hardware limits and calibration.

Hjort Creations' original contributions are provided under the [Own-Printer Use License](../LICENSE.md).
Use on your own printers, including business use and paid printing, is permitted.
Commercial redistribution requires separate permission. Earlier and third-party rights remain unchanged;
see [third-party notices](../THIRD_PARTY_NOTICES.md). Both notices accompany profile ZIPs.

## Download and import the starter bundle

**[Hjort-Creations-Modix-BIG-PrusaSlicer.ini](https://github.com/HjortCreations/modix-big-series/releases/download/v0.3.7/Hjort-Creations-Modix-BIG-PrusaSlicer.ini)**

1. In PrusaSlicer 2.9.6, choose **File > Import > Import Config Bundle** and select the downloaded file.
2. Select your **Hjort Creations - model - head/nozzle** printer preset.
3. Select **Hjort Creations - BIG Starter - Layer 0.4** and a matching **Hjort Creations** filament preset.
4. Check the selected nozzle and usable build volume, set up the physical printer/upload address locally, and slice a small test.

One download imports all 15 printer presets, one shared print preset and five filament presets (three PLA, two ePETG).
There is no user build step. Existing differently named presets are retained.
The machine needs a working config.g/homing/bed.g and the shared stop.g, cancel.g and adaptive_mesh.g first;
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
| Griffin | 0.8 | 25 | 235 / 225 | 0.015 |
| Griffin High-Flow | 0.8 | 40 | 235 / 225 | 0.015 |
| Griffin ULTRA | 1.4 | 80 | 235 / 215 | 0.035 |

These are generic PLA starting values for tuning, not measured limits for every nozzle/material.
High-Flow's conservative 40 mm³/s cap was requested by the operator; 60 is deliberately not used for High-Flow.
ULTRA 1.4 starts at the operator's conservative 80 mm³/s value; the separate 1.8 mm profile retains the operator's 100 mm³/s working setting.
All three target 45 s minimum layer time, 5 mm/s minimum print speed, no fan for the first two layers
and full fan at layer 5. The speed floor can prevent achieving 45 s on very small layers; inspect cooling in preview.
PLA temperatures, extrusion multiplier, PA and flow are intended to be tuned to the installed head/nozzle/material.

### FormFutura ePETG

The **Hjort Creations - FormFutura ePETG - Griffin** and **Hjort Creations - FormFutura ePETG - Griffin ULTRA**
filament presets are each shared by all five printer sizes with the matching head.
The shared baseline comes from the operator's ongoing 1.8 mm ULTRA tuning, with explicitly requested temperature
and flow changes for standard Griffin. The addnorth template name in the original screenshots
does not identify the material. Brand is **FormFutura**, product **ePETG**, and material type **PETG**.

| Head | First / normal temperature, °C | Max flow, mm³/s | Starting PA |
|---|---|---|---|
| Griffin | 245 / 235 | 15 | 0.015 |
| Griffin ULTRA | 245 / 245 | 70 | 0.035 |

- Bed heating remains **0 °C**; extrusion multiplier **1**, diameter **1.75 mm**, density **1.27 g/cm³** from the supplied baseline.
- Automatic cooling and fan-always-on enabled: **30–75%** normal fan, **100%** bridge fan, fan disabled for the first **3 layers**, full-fan-layer setting **0**.
- Retain the screenshot's **15 s** fan threshold, but use the operator-confirmed **45 s** slowdown target and **5 mm/s** speed floor instead of the template's 10 s / 15 mm/s.
- PA uses each head's starting value; neither value is a measured ePETG PA calibration.

The template's 29.99 material cost is not a verified FormFutura price, so cost is left at zero for local entry.
This is a working starting profile, not a completed material/nozzle validation. Confirm flow on other nozzles.
Dependencies offer each ePETG preset alongside PLA only for its matching head. High-Flow has no ePETG preset yet.

The shared process uses automatic widths (all width fields zero), 0.4 mm layers/first layer, two walls,
15% adaptive cubic infill and the existing shared start/end sequence. Infill combination is disabled for this baseline.
Print/travel acceleration stays 250/800; feature acceleration overrides stay zero.
Shared print defaults use 10% infill/perimeter overlap, a 0.95 bridge flow ratio and 0.05 mm G-code resolution
with G2/G3 I/J arc fitting enabled. These defaults also apply to the independent and example profiles.
Axis speed limits remain in the printer firmware. Slicer machine limits are used only for time estimation.
The selected filament preset supplies PA in its filament start G-code, after the shared printer startup.
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
