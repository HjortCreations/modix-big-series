# Installing an example combination package

For individual features, use the [macro instructions](../macros/README.md). For print/material presets only, use the [slicer instructions](../slicer/README.md). Neither requires a model recipe.

This page covers optional example- packages. They are **overlays**, not universal, complete machine configurations.
Keep the working Modix config.g, driver directions and currents, M584/M671 ordering,
G31, config_probe.g, PID files, heater/fan wiring and accessories.
Retain the machine's existing network settings. The build tools do not connect to the printer.

1. Back up the SD/system files and active slicer settings locally. Store the backup outside this repository.
2. Select the correct geometry, hardware and toolhead. Verify the X/Y endstop directions, four independent Z drivers and the M671 screw order.
3. Check toolhead clearance and probe offsets on the actual machine. The ULTRA's 40 mm front clearance is a working starting point from one installation, not a universal offset. Automatic Z-offset puck calibration is not included.
4. Review manifest.json. Install the sys/ files as a matching set: bed.g, g32_u.g, adaptive_mesh.g, stop.g, the axis test and the four appropriate homing files. Do not increase driver current or change wiring simply to match a model name.
5. reference/config_model.g is a comparison reference. Do not copy its M208/M671 settings over a calibrated machine without verifying travel, geometry and motor order.
6. Check the M906 idle-current factor and M84 timeout in the existing configuration. The reference installations use 50% after 100 seconds. The stop routine keeps Z enabled; the selected holding current must support the bed.
7. Read the installed files back and verify their hashes. G32 D1, the adaptive-mesh call's D1 option and the homing files' D1 modes report plans without motion.
8. Test homing, G32, mesh probing and the end sequence under supervision with a clear bed. This is a separate physical test; a successful build does not verify motion or wiring.
9. Import PrusaSlicer-bundle.ini through **File â†’ Import â†’ Import Config Bundle**, then select the three matching presets. Process/material names are shared across models; printer preset names identify geometry and toolhead. Alternatively, import the complete PrusaSlicer.ini with **Import Config**.
10. Set up the physical printer and its IP address locally in PrusaSlicer. Reslice existing jobs: older G-code still contains its original start and end commands.

Full homing and Z homing invalidate cached bed alignment; XY homing preserves it. Releasing Z makes its position unknown, so the next start homes and realigns the bed. After mechanical work, run G32 S1.
A firmware restart clears the cached state. The condition cannot detect manual adjustment of the bed screws.

The Griffin Y-min reference retains its older two-pass homing. The Y-max variant retains the latest single-pass routine. Homing consistency does not mean copying another machine's directions.
The package uses the ULTRA's explicit temperature change after the first layer for all profiles, including Griffin. Each profile changes to its configured normal printing temperature. The start/end sequence is otherwise unchanged.
