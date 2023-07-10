#!/usr/local/bin/python3
# shebang for mac osx

"""
MODULE DESCRIPTION
Generates gcode for FDM 3D printers of a hydroponics/airoponics plant root grow plug
Cylander with solid walls and internal structure being a rectiliner grid made up of single filament strands
Prints single cylinder on bed center
All print speeds and feeds are fixed at default bridging settings
G code head & foot based on Cura output for Ultimaker S5
Assumes bedXYZ is 100x100x100 by default

MODULE FEATURES
python3 3dgrowplug.py -d 40 -z 40 -g 1.75 -n 0.4 > out.g
"""

#TODO - add Extruder

# import std lib
import sys
import argparse
import math
import pprint as pp

debug = True

#get cmd line arguments
parser = argparse.ArgumentParser(prog='3dgrowplug',
  		 description='Generates gcode for FDM 3D printers of a hydroponics/airoponics plant root grow plug')
parser.add_argument('-d', '--cylinder_dia', required=True, type=float,
                    help='diameter of cylinder in mm')
parser.add_argument('-z', '--cylinder_height', required=True, type=float,
                    help='z height of cylinder in mm')
parser.add_argument('-g', '--grid_space', required=True, type=float,
                    help='internal grid spacing in mm')
parser.add_argument('-n', '--nozzle_dia', required=True, type=float,
                    help='nozzle diameter (and therefore layer height) in mm')
parser.add_argument('-b', '--bedXYZ', required=False, nargs='?', default=100, const=1, type=float,
                    help='bed length, width & height')
args = parser.parse_args()

#validate arguments
#ensure cylinder height is divisible by an even number of layer thicknesses
#add the remainder to the height
remainder = args.cylinder_height / args.nozzle_dia * 2 - float(math.trunc(args.cylinder_height / args.nozzle_dia * 2))
if remainder > 0:
	args.cylinder_height += remainder
try:
    if args.nozzle_dia <= 0 or args.nozzle_dia > 2:
      raise ValueError("nozzle diameter must be >0 <2")
    if args.cylinder_dia <= 0 or args.cylinder_dia >= args.bedXYZ:
      raise ValueError("cylinder diameter must be >0 <bed max")
    if args.cylinder_height <= 0 or args.cylinder_height >= args.bedXYZ - 5 - args.nozzle_dia:
      raise ValueError("cylinder height must be >0 <bedXYZ - 5 - nozzle diameter")
    if args.grid_space <= 0 or args.grid_space >= args.cylinder_dia:
      raise ValueError("grid spacing must be >0 <cylinder diameter")
except ValueError as err:
  print(err, file=sys.stderr)
  print('DO NOT USE THIS GCODE', file=sys.stderr)
  exit()

if debug == True:
	print(";Debug: validated inputs")
	print(";cylinder_diameter: ", args.cylinder_dia)
	print(";cylinder_height: ", args.cylinder_height)
	print(";grid_space: ", args.grid_space)
	print(";nozzle_dia: ", args.nozzle_dia)
	print(";bedXYZ: ", args.bedXYZ)

#setup other variables
clearence = 5
z_safe = args.cylinder_height + clearence #z safe height above work in mm
ccenter = args.bedXYZ / 2
rad = args.cylinder_dia / 2
#calculate grid count to ensure there is a gap at both sides of circle to avoid zero distance
grid_count = 0
#if roundly diameter is divisible by grid spacing
if args.cylinder_dia % args.grid_space == 0:
	grid_count = int((args.cylinder_dia / args.grid_space) - 2) #ignore first and last
#else if indevisible
else:
	grid_count = int(math.floor(args.cylinder_dia / args.grid_space) + 1)
layer_count = args.cylinder_height / args.nozzle_dia #number of layers
layer_heights = [] #list of z height for each layer
layer_curr = 1 #current layer
while layer_curr <= layer_count:
  layer_heights.append(args.nozzle_dia * layer_curr)
  layer_curr += 1

if debug == True:
	print()
	print(";Debug: variables")
	print(";clearence: ", clearence)
	print(";z_safe; ", z_safe)
	print(";ccenter: ", ccenter)
	print(";rad: ", rad)
	print(";grid_count: ", grid_count)
	print(";layer_count: ", layer_count)
	print(";layer_heights: ")
	for i in layer_heights:
		print(';', i)
	
#caculate coordinates on a circle using y = sqrt(r^2 - x^2)

#x
#start in top left -x +y quadrent
#move down to -x -y quadrent
#move right
#move up
#move right
#repeat to complete an x layer
#reverse x & y to create a y layer

#list x cords
x = []
x.append(-abs(grid_count / 2 * args.grid_space)) #start with left most -x value
x.append(-abs(grid_count / 2 * args.grid_space)) #duplicate for top and bottom y at each x
#incrementally add grid spacing to move to right most x value
for i in range(0, grid_count):
	x.append(x[-1] + args.grid_space)
	x.append(x[-1]) #duplicate

#list y cords
y = []
flipflop = 1
flopflip = 0
for i in x:
	if flipflop == 1 and flopflip == 0:
		y.append(abs(math.sqrt(abs(pow(rad, 2) - pow(i, 2)))))
		flipflop = 0
		flopflip = 0
	elif flipflop == 0 and flopflip == 0:
		y.append(-abs(math.sqrt(abs(pow(rad, 2) - pow(i, 2)))))
		flipflop = 1
		flopflip = 1
	elif flipflop == 1 and flopflip == 1:
		y.append(-abs(math.sqrt(abs(pow(rad, 2) - pow(i, 2)))))
		flipflop = 0
		flopflip = 1
	elif flipflop == 0 and flopflip == 1:
		y.append(abs(math.sqrt(abs(pow(rad, 2) - pow(i, 2)))))
		flipflop = 1
		flopflip = 0

#combine cords
xy = list(zip(x, y))

#reverse x & y
yx = []
for x, y in xy:
	yx.append((y, x))

if debug == True:
	print()
	print(";Debug: layer X cordinates")
	for i in xy:
		print(';', i)
	print()
	print(";Debug: layer Y cordinates")
	for i in yx:
		print(';', i)

#print header
print("""
;OUTPUT_FROM: 3dgrowplug.py
G28 XYZ         ;move all axis to home
T0              ;select extruder
M107            ;fan off
M109 S200       ;set target extruder temp in *C and wait
M190 S60        ;set target bed temp in *C and wait
M82             ;absolute extrusion mode
G90             ;absolute positioning mode
G92 E0          ;set extruder position to 0
G280 S1         ;prime nozzle
G0 Z{}          ;rapid move z to safe height
G1 F2700 E-6.5  ;move extruder back
M204 S1000      ;set starting acceleration
M205 X20 Y20    ;set motion jerk
G1 F600 X{} Y{} ;move to bed center
G92 X0 Y0       ;set XY position as 0,0
G1 F600 X{} Y{} ;move to starting position
M106 S255       ;fan on full
G1 F2700 E0     ;ready extruder
G1 F600          ;set speed""".format(z_safe, ccenter, ccenter, xy[0][0], xy[0][1]))

#nth layer
layer_heights = enumerate(layer_heights)
for layer_curr, height in layer_heights:
	print("""
;LAYER:{}X
G1 Z{}      ;move to layer z height""".format(layer_curr, height))
	for x, y in xy:
		print("G1 X{} Y{}".format(x, y))
	print("G1 Z{}      ;move to traverse height".format(height + clearence))
	print("""
;LAYER:{}Y
G1 Z{}      ;move to layer z height""".format(layer_curr, height))
	for x, y in yx:
		print("G1 X{} Y{}".format(x, y))
	print("G1 Z{}      ;move to traverse height".format(height + clearence))

#print footer
print("""
M104 T0 S0      ;turn off extruder temp
M140 S0         ;turn off bed temp
M107            ;fan off
G0 Z{}         ;rapid move z to safe height
G1 F2700 E-6.5  ;move extruder back
G28 XYZ         ;move all axis to home
;END OF FILE""".format(z_safe))