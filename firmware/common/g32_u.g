; Shared adaptive U-path Z tilt for commissioned Modix BIG machines.
; Required: RRF 3.5.3+, Cartesian X/Y/Z, BLTouch 0, four independent Z motors.
; Machine: keep its own M584/M671, G31/config_probe.g and homing files.
; Toolhead wrapper: H name; A/B/C/E nozzle insets left/front/right/rear (mm).
; D1 reports the plan and returns before any command changes state or moves.
; This macro neither selects a heated tool nor configures heaters or G31 values.

if #move.axes < 3
    abort "BIG U tilt requires X/Y/Z"
if move.axes[0].letter != "X" || move.axes[1].letter != "Y" || move.axes[2].letter != "Z"
    abort "BIG U tilt requires X/Y/Z in that axis order"
if #move.axes[2].drivers != 4
    abort "BIG U tilt currently requires four independent Z motors"
if !exists(move.kinematics.tiltCorrection.screwX)
    abort "BIG U tilt requires this machine's M671 screw coordinates"
if #move.kinematics.tiltCorrection.screwX != 4 || #move.kinematics.tiltCorrection.screwY != 4
    abort "BIG U tilt requires four M671 screw coordinates"
if #sensors.probes < 1
    abort "BIG U tilt requires probe 0"
if sensors.probes[0].type != 9
    abort "BIG U tilt requires the commissioned BLTouch probe"
if !fileexists("0:/sys/config_probe.g")
    abort "BIG U tilt requires this machine's config_probe.g"
if !exists(param.H)
    abort "Choose a Griffin or Griffin ULTRA bed.g wrapper"
if param.H != "Griffin" && param.H != "Griffin ULTRA"
    abort "Unknown BIG U tilt toolhead profile"

var inset_left = 2
var inset_front = 2
var inset_right = 2
var inset_rear = 2
if exists(param.A)
    set var.inset_left = param.A
if exists(param.B)
    set var.inset_front = param.B
if exists(param.C)
    set var.inset_right = param.C
if exists(param.E)
    set var.inset_rear = param.E
if min(var.inset_left, var.inset_front, var.inset_right, var.inset_rear) < 2
    abort "BIG U tilt nozzle insets must be at least 2 mm"

; G30 X/Y are PROBE coordinates. Subtract G31 X/Y to get nozzle coordinates.
; Intersect nozzle reach with a conservative bed rectangle inside X/Y limits.
; A negative probe offset must never put a front/left probe point off the bed.
var edge_margin = 2
var probe_left = max(move.axes[0].min + var.edge_margin, move.axes[0].min + var.inset_left + sensors.probes[0].offsets[0])
var probe_right = min(move.axes[0].max - var.edge_margin, move.axes[0].max - var.inset_right + sensors.probes[0].offsets[0])
var probe_front = max(move.axes[1].min + var.edge_margin, move.axes[1].min + var.inset_front + sensors.probes[0].offsets[1])
var probe_rear = min(move.axes[1].max - var.edge_margin, move.axes[1].max - var.inset_rear + sensors.probes[0].offsets[1])
if var.probe_right - var.probe_left < 100 || var.probe_rear - var.probe_front < 100
    abort "BIG U tilt has too little reachable probing area"
var saved_z_feed = move.axes[2].speed
var saved_z_acceleration = move.axes[2].acceleration
var saved_z_jerk = move.axes[2].jerk
var saved_probe_fast = sensors.probes[0].speeds[0]
var saved_probe_slow = sensors.probes[0].speeds[1]
var saved_probe_height = sensors.probes[0].diveHeights[0]
var saved_probe_repeat_height = sensors.probes[0].diveHeights[1]
var saved_probe_travel = sensors.probes[0].travelSpeed
var probe_travel = min(var.saved_probe_travel, move.axes[0].speed, move.axes[1].speed, 9000)
; Axis/probe speed and jerk object-model fields already use mm/min.
; The cache is valid only while Z remains homed and for the same toolhead.
; Full/Z homing files invalidate it; a restart removes these runtime globals.
var force_tilt = false
if exists(param.S)
    if param.S != 0 && param.S != 1
        abort "G32 accepts S0 (conditional) or S1 (force)"
    set var.force_tilt = param.S = 1
var cached_tilt = false
if exists(global.bigUTiltValid) && exists(global.bigUTiltHead)
    set var.cached_tilt = global.bigUTiltValid && move.axes[2].homed && global.bigUTiltHead = param.H
if exists(param.D)
    if param.D = 1
        echo "BIG U tilt profile:", param.H
        if var.cached_tilt && !var.force_tilt
            echo "Conditional G32: SKIP; Z hold and successful tilt retained"
        else
            echo "Conditional G32: RUN; no valid tilt or S1 requested"
        echo "U path: FL -> FR -> RR -> RL; following pass reverses"
        echo "Probe X:", var.probe_left, var.probe_right, "Y:", var.probe_front, var.probe_rear
        echo "Nozzle X:", var.probe_left - sensors.probes[0].offsets[0], var.probe_right - sensors.probes[0].offsets[0]
        echo "Nozzle Y:", var.probe_front - sensors.probes[0].offsets[1], var.probe_rear - sensors.probes[0].offsets[1]
        echo "Restore Z feed/accel/jerk:", var.saved_z_feed, var.saved_z_acceleration, var.saved_z_jerk
        echo "Target 0.02 mm; at most 11 passes; failed convergence aborts the job"
        M99

; D1 returns above before creating or changing globals.
if !exists(global.bigUTiltValid)
    global bigUTiltValid = false
if !exists(global.bigUTiltHead)
    global bigUTiltHead = ""
if var.cached_tilt && !var.force_tilt
    ; Direct G32 calls also home released XY axes without disturbing held Z.
    if !move.axes[0].homed
        G28 X
    if !move.axes[1].homed
        G28 Y
    echo "BIG U tilt skipped: successful tilt retained and Z still held"
    M99
; Invalidate BEFORE probing, so an interrupted or failed attempt never caches success.
set global.bigUTiltValid = false

var target_deviation = 0.02
var max_regular_passes = 10
var initial_dive_height = 15
var minimum_dive_height = 3
var clearance_margin = 3
var dive_height = var.initial_dive_height
var forward_u_path = true
var converged = false
var final_deviation = 0

; Use this machine's own calibration and homing, then remove any loaded old mesh.
M98 P"config_probe.g"
M280 P0 S60 I1
T-1 P0
G29 S2
M290 R0 S0
if !move.axes[0].homed || !move.axes[1].homed || !move.axes[2].homed
    G28
G29 S2
M558 H{var.dive_height} F600:180 T{var.probe_travel}
M203 Z600
G90
G1 Z5 F400
echo "BIG U tilt starting:", param.H

while true
    M280 P0 S60 I1
    M558 H{var.dive_height} F600:180 T{var.probe_travel}
    if iterations = 0
        M203 Z600
    else
        M203 Z{var.saved_z_feed}
    if var.forward_u_path
        G30 P0 X{var.probe_left} Y{var.probe_front} Z-99999
        G30 P1 X{var.probe_right} Y{var.probe_front} Z-99999
        G30 P2 X{var.probe_right} Y{var.probe_rear} Z-99999
        G30 P3 X{var.probe_left} Y{var.probe_rear} Z-99999 S4
        set var.forward_u_path = false
    else
        G30 P3 X{var.probe_left} Y{var.probe_rear} Z-99999
        G30 P2 X{var.probe_right} Y{var.probe_rear} Z-99999
        G30 P1 X{var.probe_right} Y{var.probe_front} Z-99999
        G30 P0 X{var.probe_left} Y{var.probe_front} Z-99999 S4
        set var.forward_u_path = true
    set var.final_deviation = abs(move.calibration.initial.deviation)
    echo "BIG U tilt pass", iterations + 1, "deviation", var.final_deviation, "mm"
    if var.final_deviation <= var.target_deviation
        set var.converged = true
        break
    if iterations >= var.max_regular_passes
        break
    set var.dive_height = min(var.initial_dive_height, max(var.minimum_dive_height, var.final_deviation + var.clearance_margin))

if var.converged
    G1 Z5 F400
    M558 H4 F600:180
    M203 Z600
    M98 P"config_probe.g"
    G28 Z

; Normal completion AND convergence-limit failure restore the original settings.
; A probe/homing/firmware fault can interrupt before this cleanup: reinitialise
; using the machine's normal recovery before trying again; no success is claimed.
G29 S2
M203 Z{var.saved_z_feed}
M201 Z{var.saved_z_acceleration}
M566 Z{var.saved_z_jerk}
M558 H{var.saved_probe_height}:{var.saved_probe_repeat_height} F{var.saved_probe_fast}:{var.saved_probe_slow} T{var.saved_probe_travel}
M400
if !var.converged
    abort "BIG U tilt did not reach 0.02 mm after 11 passes; settings restored"
set global.bigUTiltHead = param.H
set global.bigUTiltValid = true
echo "BIG U tilt complete:", param.H, "deviation", var.final_deviation, "mm; normal settings restored"
