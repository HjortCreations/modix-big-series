; Shared Modix BIG cancellation entry point; keep end behaviour in stop.g.
; RRF 3.5+ runs this file when a paused job is cancelled.
; Do not release Z or invalidate retained bed alignment here.
if exists(param.D)
    if param.D = 1
        M98 P"stop.g" D1
        M99
M98 P"stop.g"
M290 R0 S0 ; Clear the cancelled job's babystepping after parking
