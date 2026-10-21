; axis_test.g - short, cold XYZ exercise for Cartesian RepRapFirmware 3.5+.
; Run: M98 P"axis_test.g". Read-only plan: M98 P"axis_test.g" D1.
; Use on an empty bed with the normal homing routine already commissioned.
; No heating, extrusion, tuning changes, motor disable, G32 or new mesh probing.

if state.machineMode != "FFF" || move.kinematics.name != "cartesian"
    abort "axis_test.g requires a Cartesian FFF printer"
if #move.axes != 3
    abort "axis_test.g requires exactly three axes; review extra/IDEX axes first"
if move.axes[0].letter != "X" || move.axes[1].letter != "Y" || move.axes[2].letter != "Z"
    abort "axis_test.g requires axes ordered X, Y, Z"
if job.file.fileName != null
    abort "Run axis_test.g as a standalone macro, not during a print"
if !move.limitAxes || !move.noMovesBeforeHoming || move.speedFactor > 1
    abort "Enable axis limits/homing checks and set speed override to 100% or less"

; Sweep most of XY with 10% (at least 20 mm) clear of each limit.
; Z stroke is at most 50 mm, scaled/clipped for short machines.
var mx = max(20, (move.axes[0].max - move.axes[0].min) * 0.1)
var my = max(20, (move.axes[1].max - move.axes[1].min) * 0.1)
var xlo = move.axes[0].min + var.mx
var xhi = move.axes[0].max - var.mx
var ylo = move.axes[1].min + var.my
var yhi = move.axes[1].max - var.my
var xc = (var.xlo + var.xhi) / 2
var yc = (var.ylo + var.yhi) / 2
var zlo = max(20, move.axes[2].min + 20)
var zTravel = min(50, (move.axes[2].max - move.axes[2].min) * 0.25, move.axes[2].max - 10 - var.zlo)
var zhi = var.zlo + var.zTravel
if var.xhi <= var.xlo || var.yhi <= var.ylo || var.zTravel < 5 || var.zhi > move.axes[2].max - 10
    abort "Not enough configured travel for the axis test"

; Feedrates are mm/min: at most 150 mm/s XY and 5 mm/s Z,
; and at most 75% of the configured per-axis maximum speeds.
var xyFeed = min(9000, move.axes[0].speed * 0.75, move.axes[1].speed * 0.75)
var zFeed = min(300, move.axes[2].speed * 0.75)
var dx = var.xhi - var.xlo
var dy = var.yhi - var.ylo
var dz = var.zhi - var.zlo
var xyzFeed = min(var.xyFeed, var.zFeed * sqrt(var.dx * var.dx + var.dy * var.dy + var.dz * var.dz) / var.dz)
if var.xyFeed <= 0 || var.zFeed <= 0
    abort "Invalid configured maximum speeds"
echo "Axis test bounds: X", var.xlo, var.xhi, "Y", var.ylo, var.yhi, "Z", var.zlo, var.zhi
echo "Axis test feeds mm/min: XY", var.xyFeed, "Z", var.zFeed, "XYZ", var.xyzFeed
if exists(param.D)
    if param.D = 1
        echo "PLAN ONLY: no homing, motion or state changes performed"
        M99

G28                         ; use this machine's existing homeall.g
M400
if !move.axes[0].homed || !move.axes[1].homed || !move.axes[2].homed
    abort "Homing did not establish all three axis positions"
; Isolate the axes from mesh-induced Z motion, then reload the same saved mesh.
var meshActive = move.compensation.type = "mesh"
var meshFile = ""
if var.meshActive
    if move.compensation.file = null
        abort "Active mesh has no saved filename"
    set var.meshFile = move.compensation.file
    if !fileexists(var.meshFile)
        abort "Cannot reload the active mesh; axis test stopped before disabling it"
    G29 S2
G90
G53 G1 Z{var.zlo} F{var.zFeed}
G53 G1 X{var.xc} Y{var.yc} F{var.xyFeed}
M400
M117 "Axis test: X"
G53 G1 X{var.xlo} F{var.xyFeed}
G53 G1 X{var.xhi} F{var.xyFeed}
G53 G1 X{var.xc} F{var.xyFeed}
M400
M117 "Axis test: Y"
G53 G1 Y{var.ylo} F{var.xyFeed}
G53 G1 Y{var.yhi} F{var.xyFeed}
G53 G1 Y{var.yc} F{var.xyFeed}
M400
M117 "Axis test: Z"
G53 G1 Z{var.zhi} F{var.zFeed}
G53 G1 Z{var.zlo} F{var.zFeed}
M400
M117 "Axis test: XYZ"
G53 G1 X{var.xlo} Y{var.ylo} F{var.xyFeed}
G53 G1 X{var.xhi} Y{var.yhi} Z{var.zhi} F{var.xyzFeed}
G53 G1 X{var.xlo} Y{var.ylo} Z{var.zlo} F{var.xyzFeed}
G53 G1 X{var.xlo} Y{var.yhi} F{var.xyFeed}
G53 G1 X{var.xhi} Y{var.ylo} Z{var.zhi} F{var.xyzFeed}
G53 G1 X{var.xlo} Y{var.yhi} Z{var.zlo} F{var.xyzFeed}
G53 G1 X{var.xc} Y{var.yc} F{var.xyFeed}
M400
if var.meshActive
    G29 S1 P{var.meshFile}
M117 "Axis test complete"
echo "Axis test complete; parked at XY centre, Z", var.zlo
