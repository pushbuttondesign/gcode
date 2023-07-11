; HEADER
; AUTHOR: export from ggg.py
; PART #: grid-01-01
G54; Work Coordinates
G21; mm mode
G90; absolute positioning
G28 z; home z axis
;G28 x y; home x y at the same time - not used, assume set start position manually 
M3 S3000 $-1; start all spindles clockwise
F500; set feedrate

; Y AXIS
G1 Z-10.0 F200; slowly drop cutter to final cut depth
G1 X0
G1 Z-10.0 F200
G1 Y100
G0 Z0
G1 X-10
G1 Z-10.0 F200
G1 Y0
G0 Z0
G1 X-20
G1 Z-10.0 F200
G1 Y100
G0 Z0
G1 X-30
G1 Z-10.0 F200
G1 Y0
G0 Z0
G1 X-40
G1 Z-10.0 F200
G1 Y100
G0 Z0
G1 X-50
G1 Z-10.0 F200
G1 Y0
G0 Z0
G1 X-60
G1 Z-10.0 F200
G1 Y100
G0 Z0
G1 X-70
G1 Z-10.0 F200
G1 Y0
G0 Z0
G1 X-80
G1 Z-10.0 F200
G1 Y100
G0 Z0
G1 X-90
G1 Z-10.0 F200
G1 Y0
G0 Z0
G1 X-100
G1 Z-10.0 F200
G1 Y100
G0 Z0

; FOOTER
G28 z; home z axis
M5 $-1; all spindles off
G28 x y; home x y at the same time 
M2; end program
