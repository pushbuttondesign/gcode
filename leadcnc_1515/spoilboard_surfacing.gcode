; HEADER
; AUTHOR: export from ggg.py
; PART #: grid-01-01
; DESCRIPTION: for use with 25mm cutter, surfaces spoilboard
; NOTE: requires regenerating at absolute z height of lowest point
; EXPORT COMMAND: ./ggg.py -x 1195 -y -1295 --only-y --x-pitch 13 --y-pitch -13 -f 1000 -z -88.5 > ./leadcnc_1515/surface.gcode
G54; work Coordinates
G21; mm mode
G90; absolute positioning
;G28 Z0; home z axis
;G28 X0 Y0; home x y at the same time
M3 S3000; start default spindle 0 clockwise at given RPM

; Y AXIS
G1 Z-88.5 F200; cutting depth
G1 X0 F1000
G1 Y-1295 F1000
G1 X13 F1000
G1 Y0 F1000
G1 X26 F1000
G1 Y-1295 F1000
G1 X39 F1000
G1 Y0 F1000
G1 X52 F1000
G1 Y-1295 F1000
G1 X65 F1000
G1 Y0 F1000
G1 X78 F1000
G1 Y-1295 F1000
G1 X91 F1000
G1 Y0 F1000
G1 X104 F1000
G1 Y-1295 F1000
G1 X117 F1000
G1 Y0 F1000
G1 X130 F1000
G1 Y-1295 F1000
G1 X143 F1000
G1 Y0 F1000
G1 X156 F1000
G1 Y-1295 F1000
G1 X169 F1000
G1 Y0 F1000
G1 X182 F1000
G1 Y-1295 F1000
G1 X195 F1000
G1 Y0 F1000
G1 X208 F1000
G1 Y-1295 F1000
G1 X221 F1000
G1 Y0 F1000
G1 X234 F1000
G1 Y-1295 F1000
G1 X247 F1000
G1 Y0 F1000
G1 X260 F1000
G1 Y-1295 F1000
G1 X273 F1000
G1 Y0 F1000
G1 X286 F1000
G1 Y-1295 F1000
G1 X299 F1000
G1 Y0 F1000
G1 X312 F1000
G1 Y-1295 F1000
G1 X325 F1000
G1 Y0 F1000
G1 X338 F1000
G1 Y-1295 F1000
G1 X351 F1000
G1 Y0 F1000
G1 X364 F1000
G1 Y-1295 F1000
G1 X377 F1000
G1 Y0 F1000
G1 X390 F1000
G1 Y-1295 F1000
G1 X403 F1000
G1 Y0 F1000
G1 X416 F1000
G1 Y-1295 F1000
G1 X429 F1000
G1 Y0 F1000
G1 X442 F1000
G1 Y-1295 F1000
G1 X455 F1000
G1 Y0 F1000
G1 X468 F1000
G1 Y-1295 F1000
G1 X481 F1000
G1 Y0 F1000
G1 X494 F1000
G1 Y-1295 F1000
G1 X507 F1000
G1 Y0 F1000
G1 X520 F1000
G1 Y-1295 F1000
G1 X533 F1000
G1 Y0 F1000
G1 X546 F1000
G1 Y-1295 F1000
G1 X559 F1000
G1 Y0 F1000
G1 X572 F1000
G1 Y-1295 F1000
G1 X585 F1000
G1 Y0 F1000
G1 X598 F1000
G1 Y-1295 F1000
G1 X611 F1000
G1 Y0 F1000
G1 X624 F1000
G1 Y-1295 F1000
G1 X637 F1000
G1 Y0 F1000
G1 X650 F1000
G1 Y-1295 F1000
G1 X663 F1000
G1 Y0 F1000
G1 X676 F1000
G1 Y-1295 F1000
G1 X689 F1000
G1 Y0 F1000
G1 X702 F1000
G1 Y-1295 F1000
G1 X715 F1000
G1 Y0 F1000
G1 X728 F1000
G1 Y-1295 F1000
G1 X741 F1000
G1 Y0 F1000
G1 X754 F1000
G1 Y-1295 F1000
G1 X767 F1000
G1 Y0 F1000
G1 X780 F1000
G1 Y-1295 F1000
G1 X793 F1000
G1 Y0 F1000
G1 X806 F1000
G1 Y-1295 F1000
G1 X819 F1000
G1 Y0 F1000
G1 X832 F1000
G1 Y-1295 F1000
G1 X845 F1000
G1 Y0 F1000
G1 X858 F1000
G1 Y-1295 F1000
G1 X871 F1000
G1 Y0 F1000
G1 X884 F1000
G1 Y-1295 F1000
G1 X897 F1000
G1 Y0 F1000
G1 X910 F1000
G1 Y-1295 F1000
G1 X923 F1000
G1 Y0 F1000
G1 X936 F1000
G1 Y-1295 F1000
G1 X949 F1000
G1 Y0 F1000
G1 X962 F1000
G1 Y-1295 F1000
G1 X975 F1000
G1 Y0 F1000
G1 X988 F1000
G1 Y-1295 F1000
G1 X1001 F1000
G1 Y0 F1000
G1 X1014 F1000
G1 Y-1295 F1000
G1 X1027 F1000
G1 Y0 F1000
G1 X1040 F1000
G1 Y-1295 F1000
G1 X1053 F1000
G1 Y0 F1000
G1 X1066 F1000
G1 Y-1295 F1000
G1 X1079 F1000
G1 Y0 F1000
G1 X1092 F1000
G1 Y-1295 F1000
G1 X1105 F1000
G1 Y0 F1000
G1 X1118 F1000
G1 Y-1295 F1000
G1 X1131 F1000
G1 Y0 F1000
G1 X1144 F1000
G1 Y-1295 F1000
G1 X1157 F1000
G1 Y0 F1000
G1 X1170 F1000
G1 Y-1295 F1000
G1 X1183 F1000
G1 Y0 F1000
G1 X1195 F1000
G1 Y-1295 F1000

; FOOTER
G28 Z0; home z axis
M5; stop default spindle 0
G28 X0 Y0; home x y at the same time 
M2; end program
