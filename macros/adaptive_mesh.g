; Shared adaptive mesh for compatible Cartesian RepRapFirmware machines.
; Independent of model size, nozzle diameter and slicer profile.
; Optional nozzle clearances: L=left, F=front, R=right, E=rear, in mm.
; X/Y/A/B are first-layer NOZZLE bounds; M557 uses PROBE coordinates.
; D1 reports the plan before changing any state. Keep this machine's G31.
if #move.axes < 3 || #sensors.probes < 1
    abort "BIG mesh requires X/Y/Z and probe 0"
if move.axes[0].letter != "X" || move.axes[1].letter != "Y" || move.axes[2].letter != "Z"
    abort "BIG mesh requires Cartesian X/Y/Z axis order"
if sensors.probes[0].type != 9
    abort "BIG mesh requires the commissioned BLTouch"
if !exists(param.X) || !exists(param.Y) || !exists(param.A) || !exists(param.B)
    abort "BIG mesh requires first-layer bounds X Y A B"
if param.A <= param.X || param.B <= param.Y
    abort "BIG mesh received empty or reversed first-layer bounds"
var inset_left = 2
var inset_front = 2
var inset_right = 2
var inset_rear = 2
if exists(param.L)
    set var.inset_left = param.L
if exists(param.F)
    set var.inset_front = param.F
if exists(param.R)
    set var.inset_right = param.R
if exists(param.E)
    set var.inset_rear = param.E
if min(var.inset_left, var.inset_front, var.inset_right, var.inset_rear) < 2
    abort "Mesh nozzle clearances must be at least 2 mm"
var ox = sensors.probes[0].offsets[0]
var oy = sensors.probes[0].offsets[1]
; Same bed margin and selected nozzle insets as the commissioned G32 wrapper.
var safe_min_x = max(move.axes[0].min + 2, move.axes[0].min + var.inset_left + var.ox)
var safe_max_x = min(move.axes[0].max - 2, move.axes[0].max - var.inset_right + var.ox)
var safe_min_y = max(move.axes[1].min + 2, move.axes[1].min + var.inset_front + var.oy)
var safe_max_y = min(move.axes[1].max - 2, move.axes[1].max - var.inset_rear + var.oy)
if var.safe_max_x - var.safe_min_x < 60 || var.safe_max_y - var.safe_min_y < 60
    abort "BIG mesh has insufficient reachable probing area"
; Expand by 30 mm, with a minimum 60 mm window for parts near an edge.
var mesh_min_x = max(var.safe_min_x, min(param.X + var.ox - 30, var.safe_max_x - 60))
var mesh_max_x = min(var.safe_max_x, max(param.A + var.ox + 30, var.mesh_min_x + 60))
var mesh_min_y = max(var.safe_min_y, min(param.Y + var.oy - 30, var.safe_max_y - 60))
var mesh_max_y = min(var.safe_max_y, max(param.B + var.oy + 30, var.mesh_min_y + 60))
var mesh_width = var.mesh_max_x - var.mesh_min_x
var mesh_depth = var.mesh_max_y - var.mesh_min_y
var points_x = 3
var points_y = 3
if var.mesh_width > 150
    set var.points_x = 4
if var.mesh_width > 300
    set var.points_x = 5
if var.mesh_width > 450
    set var.points_x = 7
if var.mesh_depth > 150
    set var.points_y = 4
if var.mesh_depth > 300
    set var.points_y = 5
if var.mesh_depth > 450
    set var.points_y = 7
echo "BIG mesh probe bounds:", var.mesh_min_x, var.mesh_max_x, var.mesh_min_y, var.mesh_max_y
echo "BIG mesh grid:", var.points_x, var.points_y
if exists(param.D)
    if param.D = 1
        M99
if !move.axes[0].homed || !move.axes[1].homed || !move.axes[2].homed
    abort "Home all axes before adaptive mesh"
G29 S2 ; Remove the previously loaded mesh
M557 X{var.mesh_min_x, var.mesh_max_x} Y{var.mesh_min_y, var.mesh_max_y} P{var.points_x, var.points_y}
G29 S0 ; Probe, save and activate this print's mesh
