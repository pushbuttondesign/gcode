G54; Work Coordinates
G21; mm mode
G90; absolute positioning
G28 z; home z axis
;G28 x y; home x y at the same time - not used, assume set start positoin manually 
G0 Z5; rapid move to specified safe z height
M3 S3000 $-1; start all spindles clockwise
F3000; set feedrate

; X AXIS
G1 Z0 F500; slowly drop cutter into work piece
G1 Y0
G1 X100
G1 Y10
G1 X0
G1 Y20
G1 X100
G1 Y30
G1 X0
G1 Y40
G1 X100
G1 Y50
G1 X0
G1 Y60
G1 X100
G1 Y70
G1 X0
G1 Y80
G1 X100
G1 Y90
G1 X0
G1 Y100
G1 X100
G1 Y100
G1 X0
G0 Z5; rapid lift cutter
G0 Y0; rapid reset y

; Y AXIS
G1 Z0 F500; slowly drop cutter into work piece
G1 X0
G1 Y100
G1 X10
G1 Y0
G1 X20
G1 Y100
G1 X30
G1 Y0
G1 X40
G1 Y100
G1 X50
G1 Y0
G1 X60
G1 Y100
G1 X70
G1 Y0
G1 X80
G1 Y100
G1 X90
G1 Y0
G1 X100
G1 Y100
G1 X100
G1 Y0

G28 z; home z axis
M5 $-1; all spindles off
G28 x y; home x y at the same time 
M2; end program
