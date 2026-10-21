# Reusable printer macros

These are independent features. You do not need a machine recipe or a slicer profile to download them.
Machine size and nozzle diameter do not select a different stop routine or adaptive-mesh algorithm.
Compatibility is defined by the firmware, configured axes, probe and tool mapping described below.

| Feature | Direct source | What it adds |
|---|---|---|
| Print-end routine | [stop.g](stop.g) | Warm-tool retraction guard, bounded bed lowering, X1 Y1 parking and retained Z holding |
| Adaptive mesh | [adaptive_mesh.g](adaptive_mesh.g) | A probing grid around the print, calculated from configured travel and probe offsets |
| Adaptive U-tilt | [g32_u.g](g32_u.g) | Alternating U-shaped passes, adaptive probe depth and conditional reuse of successful alignment |
| Cold axis test | [axis_test.g](axis_test.g) | Exercises most of XY and a short Z stroke using configured limits |

Ready-to-copy files and the shared-macros ZIP are available under
[Releases](https://github.com/HjortCreations/modix-big-series/releases).
Copy the selected files to the printer's existing sys/ directory after backing up the originals.
Keep the working config.g, wiring, homing directions, probe calibration and PID values.

## stop.g

This is one shared file, including when the printer is BIG-60, BIG-120Z, BIG-Meter or BIG-180X.
It reads the configured Z maximum and the selected tool's heater mapping at runtime.
It does not depend on nozzle size, material or the print's slicer profile.

The routine targets the standard BIG-series Cartesian XYZ/tool/fan mapping on RepRapFirmware 3.5.3+.
It retracts only with a selected extruding tool whose mapped heaters are warm, turns off tool heating
and part cooling, lowers the bed towards at least Z300 with 5 mm clearance where possible,
parks at machine X1 Y1 when XY is homed, and releases XY/extruders while keeping Z enabled.
It never lowers the bed beyond configured Z-max or raises it to reach Z300.
Retained Z holding depends on the machine's configured idle current supporting the bed.

Use the same slicer end sequence regardless of model or nozzle:

```gcode
M400                       ; Finish queued moves
M300 S222 P1111             ; Print-complete notification
M0                         ; Run stop.g while the tool is still selected
```

`M98 P"stop.g" D1` reports a plan without heating, motion or modal changes.

## Adaptive mesh

The single adaptive_mesh.g file works across machine sizes. It requires Cartesian XYZ axes,
RepRapFirmware 3.5.3+, a commissioned BLTouch as probe0 and a reachable bed area described by the configured limits.
It does not require four independent Z motors or the U-tilt routine.

Pass the first-layer **nozzle** bounds. The routine converts them to probe coordinates,
adds a 30 mm margin, clips the result to the reachable area and chooses a 3–7 point grid per axis.
All axes must already be homed. Perform any bed alignment required by your machine beforehand.

Example call; numbers describe a sample print, not a particular machine model:

```gcode
M98 P"adaptive_mesh.g" X100 Y100 A250 B200
```

Optional nozzle clearances are L=left, F=front, R=right and E=rear, in millimetres.
Defaults are 2 mm on each side. The existing ULTRA setup uses a 40 mm front clearance:

```gcode
M98 P"adaptive_mesh.g" X100 Y100 A250 B200 L2 F40 R2 E2
```

Use D1 to inspect the calculated plan without changing the grid or moving.
Verify the clearances on the actual installation; the toolhead name does not establish its probe offsets.
The shared slicer start template supplies the first-layer bounds and selected head clearances automatically.

## Conditional U-tilt

This feature requires four independently driven Z motors, matching M671 screw coordinates,
Cartesian XYZ, BLTouch probe0/servo0 and the machine's own config_probe.g and homing routines.
Those requirements, rather than a BIG model name or nozzle diameter, define compatibility.

Install g32_u.g and choose bed-griffin.g, bed-griffin-high-flow.g or bed-griffin-ultra.g from the shared ZIP.
Copy the selected wrapper as sys/bed.g. The wrapper selects head clearance; the core reads machine geometry at runtime.

For cached alignment to remain valid, add this hook before motion/probing in the existing
homeall.g and homez.g. Keep each machine's original wiring and homing directions:

```gcode
if exists(global.bigUTiltValid)
    set global.bigUTiltValid = false
```

Full/Z homing invalidates alignment; XY-only homing preserves it. Releasing Z or restarting firmware prevents reuse.
Use G32 for conditional alignment, G32 S1 to force alignment and G32 D1 to inspect the plan.
After mechanical adjustment, force realignment; software cannot detect manually moved bed screws.

The routines have automated numeric/logic checks and prior installation-specific observations.
This is not a claim that every BIG model has been physically tested. Test newly installed files under supervision.
