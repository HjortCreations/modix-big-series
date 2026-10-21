; Shared Modix BIG end-of-job routine: firmware/common/stop.g.
; Generated copies must match this source; no machine-specific calibration here.
; Keep Modix cooling; park at machine X1 Y1 after the bounded Z lowering.
; D1 reports the plan before any heater, motion or modal change.
var canRetract = false
if state.currentTool >= 0
    if #tools[state.currentTool].extruders > 0 && #tools[state.currentTool].heaters > 0
        var warm = true
        var heaterIndex = 0
        while var.heaterIndex < #tools[state.currentTool].heaters
            if heat.heaters[tools[state.currentTool].heaters[var.heaterIndex]].current < heat.coldRetractTemperature
                set var.warm = false
            set var.heaterIndex = var.heaterIndex + 1
        set var.canRetract = var.warm
var parkDeltaZ = 0
if move.axes[2].homed
    ; Add clearance if room remains, and park at least Z300 without moving up.
    set var.parkDeltaZ = max(0, min(move.axes[2].max, max(300, move.axes[2].machinePosition + 5)) - move.axes[2].machinePosition)
if exists(param.D)
    if param.D = 1
        echo "BIG stop plan: retract allowed", var.canRetract, "positive Z delta", var.parkDeltaZ
        echo "BIG stop: cool T0 heaters; park X1 Y1 only if X/Y homed"
        M99
M400
if var.canRetract
    M83
    G1 E-3 F2400 ; Retract only with a selected tool and warm heaters
M568 P0 R0 S0 A0 ; Cool all heaters mapped to the primary tool
if exists(global.printheads)
    if global.printheads = 2
        M568 P1 R0 S0 A0
M106 P0 S0 ; Stop part cooling; leave the thermostatic heatsink fan controlled
T-1 P0
G29 S2 ; Park in machine coordinates without mesh-driven Z changes
M400
; Re-read settled, uncompensated Z before calculating the actual move.
set var.parkDeltaZ = 0
if move.axes[2].homed
    set var.parkDeltaZ = max(0, min(move.axes[2].max, max(300, move.axes[2].machinePosition + 5)) - move.axes[2].machinePosition)
G91
if var.parkDeltaZ > 0
    G1 Z{var.parkDeltaZ} F{min(400, move.axes[2].speed)}
    M400
if move.axes[0].homed && move.axes[1].homed
    G90
    G53 G1 X1 Y1 F6000 ; Front-left park in machine coordinates
    M400
else
    echo "BIG XY parking skipped: X or Y is not homed"
M84 X Y E0:1 ; Release XY and extruders; retain Z hold at the configured idle current
