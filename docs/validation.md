# Validation status

Compatibility is based on firmware, configured axes, probe and hardware requirements, not model/nozzle example names. Physical test coverage is a separate statement.

The components come from previously working profiles and requested macro changes.
The tools in this repository do not operate a printer.

- Shared start/end G-code retains the existing command sequence; numeric values come from the selected components.
- The U-tilt core and stop.g reuse the latest shared sources. Retraction conditions, Z-max handling and X1 Y1 parking are preserved.
- For ULTRA 1.8 mm, the operator reports working settings of 100 mmÂ³/s, 235/215 Â°C and PA 0.035. These are not measured maximum-throughput results.
- Conditional U-tilt was previously tested physically on one four-Z-motor installation. This does not establish commissioning of every new combination.
- The new packages have been built and checked offline. No system files were uploaded and no firmware was restarted during migration.
- The recently introduced X-min/Y-max single-pass homing and latest X1 Y1 end sequence still require physical observation on each installation.

## Reproducible checks

python tools/check.py verifies that shared macros and print/material profiles build without reading any model, hardware or motion recipe. It also checks byte-identical stop.g and adaptive_mesh.g across example packages, composition, shared sources, privacy,
U-tilt geometry across probe offsets and axis limits, positive and bounded Z parking,
warm-tool retraction, cache conditions, and reuse of ULTRA process/material settings across machine sizes.
GitHub Actions runs the same checks and builds the packages.

Run actual slicer validation with PrusaSlicer 2.9.6:

```console
python tools/validate_slicer.py --slicer "/path/to/prusa-slicer-console.exe" --workdir "/path/outside/repo"
```

This loads the generated complete INI, slices a locally generated model and checks
start/end commands, conditional homing, heater temperature changes, acceleration commands and flow limits.
Bundle sections are also checked for matching settings and preset identities.
Reports are saved in the work directory rather than as additional dated repository documents.
Record physical tests, motor noise, temperature margins and print quality in private service records.
