( cuts a 30mm square for calibrating steps/mm )
( 12.7 diameter cutter )
( 90x90x20mm stock )
( G54 zero must be set as cutter center at )
( bottom left corner of stock )
( mm absolute work cordinate system used )

G21 G90 G54 ; mm absolute work cordinate system
G61 G40 ; maximum accuracy settings

G0 Z5 ; move z to safe height
G0 X-36.35 Y-36.35 ; move to starting point for cut

G0 Z1 ; fast move cutter down
G1 F300 Z-5 ; drop cutter to first cut height
G1 F600 Y-53.65 ; cut square
G1 F600 X-53.65
G1 F600 Y-36.35
G1 F600 X-36.35

G1 Z-7.5 ; drop to second cut height
G1 F600 Y-53.65 ; cut square
G1 F600 X-53.65
G1 F600 Y-36.35
G1 F600 X-36.35

G0 Z10 ; raise to safe z height
M30 ; end program
