# Components and changes

Change each setting in one place. Shared macros and independent slicer profiles are the main entry points. A recipe is an optional integration example, not a prerequisite or compatibility list.

| Change | Source |
|---|---|
| Shared print-end behaviour | macros/stop.g |
| Cancel entry point (delegates to stop.g) | macros/cancel.g |
| Shared start/end sequence | slicer/gcode/ |
| Work envelope or Z-screw geometry | config/models/ |
| Travel limits for an individual machine | A local recipe outside Git, using axis_max |
| Toolhead movement/probing clearance | config/toolheads/; a local nozzle_insets_mm override if needed |
| PID, BLTouch offsets, skew, input shaping | Private machine calibration; never a toolhead default |
| Stepper model and TMC parameters | config/motors/ + firmware/motors/; requires an explicit choice |
| Axis speed limits in optional example start code | config/motion/ |
| Default travel acceleration | slicer/common/startup.json |
| Slicer time estimates | The motion component's slicer_time_estimates; these do not configure firmware |
| Layers, walls, infill, print acceleration | slicer/processes/ |
| Retraction and nozzle size | slicer/toolheads/ |
| Temperature, flow, fan and pressure advance | slicer/materials/ |
| Ready-to-import starter choices | slicer/starter.json |
| Sourced starter model sizes; no firmware geometry | slicer/machines.json |

The starter is one generated INI with all supported model/head combinations. Never maintain 15 hand-edited copies.
Process/material/nozzle components can use a base component within the same group; the builder resolves inheritance.
Dependencies use stable family/head markers in printer_notes, not display names, customer names or a list of model names.
The starter's selected filament emits its PA; earlier independent/example packages retain their existing PA placement.

Build local overrides with python tools/build.py --recipe FILE --output DIRECTORY.
Store local files outside Git or under the ignored local/ directory. Their data appears in the local package manifest, not in the repository or published release packages.

The BIG-120Z+ULTRA example reuses the same process, material and nozzle components as BIG-Meter+ULTRA.
Motion limits come from the selected motion component. The example requires separate commissioning and testing.

A new BIG size does not need a new stop.g, adaptive-mesh file or head/material profile.
Add a model geometry or full integration example only when that separate preset/overlay is needed and its geometry, motor order, homing and clearance are known.

Keep original machine baselines, individual calibration, vendor references and service/test evidence
in private service records outside this repository. Earlier service archives remain private.
The reusable components are maintained here; historical experiments are not universal defaults.
Public installation instructions and downloads must be usable without access to a private archive.
