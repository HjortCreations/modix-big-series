; Build plate heaters are not used
M104 S[first_layer_temperature] ; Start heating the nozzle without waiting
{"if !move.axes[2].homed"}
    G28                     ; Home all axes when Z position is unknown
else
    G28 X Y                 ; Rehome XY while preserving held Z and its tilt state
G32                         ; Run the configured bed alignment in bed.g
M98 P"adaptive_mesh.g" X{first_layer_print_min[0]} Y{first_layer_print_min[1]} A{first_layer_print_max[0]} B{first_layer_print_max[1]} L@LEFT@ F@FRONT@ R@RIGHT@ E@REAR@ ; Probe and enable a mesh around this print
T0                          ; Select the primary Griffin tool after homing and probing
M204 P@PRINT_ACCEL@ T@TRAVEL_ACCEL@ ; Print / travel acceleration, mm/s^2
@MAX_FEEDRATE@ ; Axis limits, mm/min
M572 S@PA@ ; Pressure advance for the selected material and toolhead
M109 S[first_layer_temperature] ; Wait for the nozzle to reach the first-layer temperature
