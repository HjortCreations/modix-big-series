# Components and changes

Change each setting in one place. A recipe selects components; it does not duplicate the entire configuration.

| Change | Source |
|---|---|
| Shared print-end behaviour | firmware/common/stop.g |
| Shared start/end sequence | slicer/gcode/ |
| Work envelope or Z-screw geometry | config/models/ |
| Travel limits for an individual machine | A local recipe outside Git, using axis_max |
| Toolhead movement/probing clearance | config/toolheads/; a local nozzle_insets_mm override if needed |
| PID, BLTouch offsets, skew, input shaping | Private machine calibration; never a toolhead default |
| Stepper model and TMC parameters | config/motors/ + firmware/motors/; requires an explicit choice |
| Axis speed limits / travel acceleration | config/motion/ |
| Slicer time estimates | The motion component's slicer_time_estimates; these do not configure firmware |
| Layers, walls, infill, print acceleration | slicer/processes/ |
| Retraction and nozzle size | slicer/toolheads/ |
| Temperature, flow, fan and pressure advance | slicer/materials/ |

Build local overrides with python tools/build.py --recipe FILE --output DIRECTORY.
Store local files outside Git or under the ignored local/ directory. Their data appears in the local package manifest, not in the repository or published release packages.

The BIG-120Z+ULTRA example reuses the same process, material and nozzle components as BIG-Meter+ULTRA.
Motion limits come from the selected motion component. The example requires separate commissioning and testing.

Add BIG-60/120X/180X variants only when geometry, motor order, homing and clearance have been established.
This repository does not contain speculative full configurations for those machines.

Unmodified originals, service history and abandoned calibration tests remain in the previous private archive.
This repository starts a new Git history without that customer data. The previous repository is preserved.
