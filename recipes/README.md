# Optional machine combination examples

These recipes demonstrate how reusable components can be assembled with a specific printer preset and hardware overlay.
They are integration examples, not compatibility restrictions on stop.g, adaptive mesh, U-tilt or slicer profiles.

| Example | Work envelope, mm | Head / nozzle | Process / material |
|---|---|---|---|
| big-120z-griffin-0.6 | 600 × 600 × 1200, V4 reference | Griffin0.6 mm | 0.2 mm / PLA |
| big-meter-griffin-0.8 | 980 × 1000 × 1000, V4 reference | Griffin0.8 mm | 0.4 mm / addnorth ePLA |
| big-meter-ultra-1.8 | 965 × 980 × 1000, upgraded legacy variant | ULTRA1.8 mm | 1.0 mm / FormFutura ePLA |

Each recipe selects independent components. The same ULTRA process/material components can be selected for another machine.
Example travel dimensions and homing directions are references, not universal values for every unit of a model.

The example- ZIPs include complete PrusaSlicer configurations and matching system-file overlays.
They do not replace the existing working config.g or contain individual probe/PID/network calibration.
See the [example-package installation guide](../docs/installation.md).

To use a shared macro, start at [macros/](../macros/README.md).
To use print/material presets with your own machine preset, start at [slicer/](../slicer/README.md).
Neither route requires adding a model recipe.
