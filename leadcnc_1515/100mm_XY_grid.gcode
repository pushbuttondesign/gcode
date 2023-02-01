; HEADER
; AUTHOR: export from ggg.pyi by steve on 31/01/23
; PART #: grid-01-01
; DESCRIPTION: cuts a 100mm spaced XY grid onto leadCNC 1515 spoil board using 45* 'V' cutter
;              z height and xy extends are -97.06Z, 1195X, -1295Y so check these beforehand 
;              cutter at approx. 20k rpm recommended
G54; work Coordinates
G21; mm mode
G90; absolute positioning
;G28 Z0; home z axis - not used, assume set start position manually
;G28 X0 Y0; home x y at the same time - not used, assume set start position manually 
M3 S20000; start default spindle 0 clockwise at given RPM

; X AXIS
G1 Z-97.06 F200; slowly drop cutter to final cut depth
G1 Y0 F2000
G1 X1195 F2000
G1 Y-100 F2000
G1 X0 F2000
G1 Y-200 F2000
G1 X1195 F2000
G1 Y-300 F2000
G1 X0 F2000
G1 Y-400 F2000
G1 X1195 F2000
G1 Y-500 F2000
G1 X0 F2000
G1 Y-600 F2000
G1 X1195 F2000
G1 Y-700 F2000
G1 X0 F2000
G1 Y-800 F2000
G1 X1195 F2000
G1 Y-900 F2000
G1 X0 F2000
G1 Y-1000 F2000
G1 X1195 F2000
G1 Y-1100 F2000
G1 X0 F2000
G1 Y-1200 F2000
G1 X1195 F2000
G1 Y-1295 F2000
G1 X0 F2000

; Y AXIS
G1 Z-97.06 F200; slowly drop cutter to final cut depth
G1 X0 F2000
G1 Y0 F2000
G1 X100 F2000
G1 Y-1295 F2000
G1 X200 F2000
G1 Y0 F2000
G1 X300 F2000
G1 Y-1295 F2000
G1 X400 F2000
G1 Y0 F2000
G1 X500 F2000
G1 Y-1295 F2000
G1 X600 F2000
G1 Y0 F2000
G1 X700 F2000
G1 Y-1295 F2000
G1 X800 F2000
G1 Y0 F2000
G1 X900 F2000
G1 Y-1295 F2000
G1 X1000 F2000
G1 Y0 F2000
G1 X1100 F2000
G1 Y-1295 F2000
G1 X1195 F2000
G1 Y0 F2000

; FOOTER
G28 Z0; home z axis
M5; stop default spindle 0
G28 X0 Y0; home x y at the same time 
M2; end program
