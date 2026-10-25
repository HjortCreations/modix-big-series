# Modix BIG Series by Hjort Creations

Reusable printer macros and independent slicer profiles for the Modix BIG series.
Choose the feature you need. A machine example's name does not limit a shared feature to that model or nozzle.

Maintained by **[Hjort Creations](https://hjortcreations.se)**, based on practical printer setup, service and tuning.
This is an independent project; it is not an official Modix firmware release.

**Want help with your printer?** We offer paid setup, service, troubleshooting, slicer tuning and training
for individuals, companies and organisations. [See how we can help](#setup-service-and-tuning).

## Get started in PrusaSlicer

**[Download the ready-to-import Hjort Creations BIG starter bundle](https://github.com/HjortCreations/modix-big-series/releases/download/v0.3.7/Hjort-Creations-Modix-BIG-PrusaSlicer.ini)**

Import the file with **File > Import > Import Config Bundle**. Select your printer/head,
the **Hjort Creations - BIG Starter - Layer 0.4** print profile and a matching filament profile.
No scripts or building are needed. The file contains:

- 15 printer presets: BIG-60, BIG-120X, BIG-120Z, BIG-180X and BIG-Meter, each with Griffin 0.8, Griffin High-Flow 0.8 and ULTRA 1.4.
- One shared print profile with automatic line widths, 0.4 mm layers and first layer, and 250/800 mm/s² print/travel acceleration in start G-code.
- Three generic PLA starting profiles: Griffin **25**, High-Flow **40** and ULTRA **80 mm³/s**. Each targets **45 s** minimum layer time with a 5 mm/s minimum print speed.
- **FormFutura ePETG for ULTRA:** 245 °C, **70 mm³/s**, 30–75% fan, 100% bridge fan and the same 45 s / 5 mm/s cooling limits. The fan is off for the first three layers.
- **FormFutura ePETG for standard Griffin:** **245 °C first layer / 235 °C normal layers**, **15 mm³/s**, with the same ePETG fan and cooling settings. Dependencies select the matching head across machine sizes.
- Dependencies matching each filament profile to its head across machine sizes. Incompatible selections can still be overridden manually.

The machine must already have the shared stop.g, cancel.g and adaptive_mesh.g installed and a working bed.g.
This slicer file does not install firmware or change the machine's own axis speed limits.
[Setup, dimensions and starting-value notes](slicer/README.md)

## Printer macros — use independently

| Feature | Open the file | Purpose |
|---|---|---|
| Shared print end | **[stop.g](macros/stop.g)** | Guard warm retraction, lower the bed within Z limits, park X1 Y1 and keep Z holding |
| Cancel a print | **[cancel.g](macros/cancel.g)** | Route cancellation through the same stop.g; retain Z holding for the next print |
| Adaptive mesh | **[adaptive_mesh.g](macros/adaptive_mesh.g)** | Probe around this print using configured travel, probe offsets and head clearance |
| Adaptive U-tilt | [g32_u.g](macros/g32_u.g) | Align a four-motor bed using alternating U paths and adaptive probe depth |
| Cold movement test | [axis_test.g](macros/axis_test.g) | Test configured XYZ motion without heating or extrusion |

**The same stop.g and adaptive_mesh.g files are used across machine sizes and nozzle diameters.**
They read the machine's configured values at runtime. No BIG-60, BIG-120Z, BIG-Meter or BIG-180X recipe is needed to download or use them.

[Macro instructions and compatibility requirements](macros/README.md) · [Download individual files or shared-macros.zip](https://github.com/HjortCreations/modix-big-series/releases)

Compatibility depends on the actual firmware, axes, probe and tool mapping. Adaptive mesh needs compatible Cartesian RepRapFirmware and a commissioned probe; U-tilt additionally needs four independently driven Z motors. Physical test coverage is documented separately.

## Slicer profiles — choose by head, nozzle and material

The all-in-one starter above is the simplest starting point. The independent packages below
preserve earlier, more specific setups for users who already have a printer preset.

| Independent profile | Process | Material |
|---|---|---|
| Griffin 0.6 mm | 0.2 mm layers | PLA |
| Griffin 0.8 mm | 0.4 mm layers | addnorth ePLA |
| Griffin ULTRA 1.8 mm | 1.0 mm layers | FormFutura ePLA |

**A ULTRA process/material profile is the same on BIG-60, BIG-Meter, BIG-180X or another compatible BIG size.**
The printer preset supplies machine geometry and hardware limits separately.
The profile packages contain print/material presets, shared start/end snippets and head settings without firmware or model geometry.

[Slicer instructions](slicer/README.md) · [Download profile ZIP packages](https://github.com/HjortCreations/modix-big-series/releases)

The current ULTRA 1.8 mm/ePLA defaults are 100 mm³/s, 235/215 °C, PA 0.035,
print/travel acceleration 250/800 mm/s², 1.0 mm layers and a 1.2 mm first layer.
These are working defaults for that head/nozzle/material, independent of bed size, not a measured maximum throughput.
Shared print defaults use 10% infill/perimeter overlap, a 0.95 bridge flow ratio and 0.05 mm G-code resolution with arc fitting enabled.

## Machine configuration and optional examples

Keep each machine's working configuration: dimensions, wiring, motor mapping, hardware limits, probe offset and PID calibration.
Individual calibration and network settings stay outside this repository.

[Machine combination examples](recipes/README.md) assemble the independent components with particular geometry and homing references.
The example ZIPs are convenient complete combinations. **They are not a list of the models that can use the shared macros or slicer profiles.**
Their newly assembled files have not been physically commissioned as complete packages.

## Feedback and bug reports

[Report a problem](https://github.com/HjortCreations/modix-big-series/issues/new/choose)
with the downloaded version, printer/controller/firmware, printhead/nozzle and what happened.
The form asks for the relevant details; remove private information before attaching files.
Suggestions are welcome through a regular issue. Individual printer setup and tuning can be arranged below.

## License and permitted use

Hjort Creations' original contributions use the [Own-Printer Use License](LICENSE.md).
Use and adapt them on your own printers, including for business and paid printing.
Commercial redistribution, resale or bundling requires separate written permission.
Noncommercial sharing must retain the license, attribution and notices.
This is a source-available project with commercial redistribution restrictions.

**Earlier CC0 permissions and third-party rights remain unchanged.**
[Third-party notices](THIRD_PARTY_NOTICES.md) identify the Modix-derived homing references,
whose upstream redistribution permission remains unresolved. The new license does not grant rights in those portions.

## Setup, service and tuning

**Hjort Creations offers paid, hands-on help getting your printer ready for everyday use.**
We work with private owners, businesses, universities and other organisations.

- Printer assembly, commissioning, mechanical service and troubleshooting.
- Firmware and macro setup for the machine's actual hardware.
- Slicer profiles, material tuning and operator training.
- CAD, prototypes and large-format 3D printing when you need parts made.

For help with a Modix printer, include the model, controller/firmware, printhead, nozzle size and what you want to improve.
We can then agree the scope and provide a quote. Service work and individual support are arranged separately from the repository downloads.

**[Contact Per about your printer](https://www.hjortcreations.com/kontakt)** ·
[Services](https://www.hjortcreations.com/tjanster) ·
[Service agreements](https://www.hjortcreations.com/butik/serviceavtal-3d-skrivare) ·
[Website and shop](https://hjortcreations.se)

## Build and maintain

Requires Python 3.10+; no additional Python packages. Output goes to the ignored dist/ directory.

```console
python tools/check.py
python tools/build.py --starter
python tools/build.py --macros
python tools/build.py --profiles
python tools/build.py --all
```

- macros/: the single source for shared printer routines.
- slicer/: shared defaults, head/nozzle settings, processes, materials and start/end G-code.
- config/: separate model, hardware, head-clearance and motor/motion references.
- recipes/: optional example combinations of those components.

[Maintenance rules](AGENTS.md) · [Where to make changes](docs/maintenance.md) · [Validation status](docs/validation.md)
