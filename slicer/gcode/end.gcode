M400                       ; Wait for all queued moves to finish
M300 S222 P1111             ; Sound the print-complete notification
M0                         ; Run Modix stop.g: retract if allowed, cool down and park
