#!/usr/local/bin/python3
# shebang for mac osx

"""
MODULE DESCRIPTION
Generates gcode for FDM 3D printers of a hydroponics/airoponics plant root grow plug
Cylander with solid walls and internal structure being a rectiliner grid made up of single filament strands
Prints single cylinder on bed center
All print speeds and feeds are fixed at default bridging settings
Assumes bedXYZ is 100x100x100 by default

MODULE FEATURES
python3 3dgrowplug.py -d 40 -z 40 -g 1.75 -n 0.4 -b 240 > 3dplugtest.gcode
"""

#TODO - add Extruder

# import std lib
import sys
import argparse
import math
import pprint as pp

debug = False

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
euclidian_dist = 0
flow_mod_per = 200
filament_dia = 2.8
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
	print(";extruder_euclidian_distance: ", euclidian_dist)
	print(";flow_modifier_percent: ", flow_mod_per)
	print(";filament_dia: ", filament_dia)
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

#reverse x & y for 90* rotated grid ontop
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
		
#off set everything by ccenter because ultimaker G92 not working
xy2 = []
for x, y in xy:
	xy2.append((x + ccenter, y + ccenter))
xy = xy2
yx2 = []
for x, y in yx:
	yx2.append((x + ccenter, y + ccenter))
yx = yx2

#print header
print("""
;OUTPUT_FROM: 3dgrowplug.py
G28 XYZ         ;move all axis to home
T0              ;select extruder
M107            ;fan off
M109 S200       ;set target extruder temp in *C and wait
M190 S60        ;set target bed temp in *C and wait
M82             ;absolute extrusion mode - only option on ultimaker S5
G90             ;absolute positioning mode
G92 E0          ;set extruder position to 0
G280 S1         ;prime nozzle
G0 Z{}          ;rapid move z to safe height
G1 F2700 E-6.5  ;move extruder back
M204 S1000      ;set starting acceleration
M205 X20 Y20    ;set motion jerk
G1 F600 X{} Y{} ;move to bed center
;G92 X0 Y0       ;set XY position as 0,0 - option broken on ultimaker S5
M106 S255       ;fan on full
G1 F2700 E0     ;ready extruder
G1 F600          ;set speed""".format(z_safe, ccenter, ccenter))

#nth layer
heights = enumerate(layer_heights)
for layer_curr in range(0,int(len(layer_heights)/2)):
	height = next(heights)
	
	print("""
;LAYER:{}X
G1 Z{}      ;move to layer z height
G1 X{} Y{} ;move to starting position""".format(layer_curr, height[1], xy[0][0], xy[0][1]))
	for i in range(1,len(xy)-1):
	
		#https://3dprinting.stackexchange.com/questions/6289/how-is-the-e-argument-calculated-for-a-given-g1-command
		euclidian_dist += math.sqrt(pow(xy[i+1][0]-xy[i][0],2)+pow(xy[i+1][1]-xy[i][1],2))/1000
		
		print("G1 X{} Y{} E{}".format(xy[i][0], xy[i][1],
			 (4*args.nozzle_dia*flow_mod_per*args.nozzle_dia*euclidian_dist)/(math.pi*pow(filament_dia/2,2))))
			 
	print("G1 Z{}      ;move to traverse height".format(height[1] + clearence))
	height = next(heights)
	
	print("""
;LAYER:{}Y
G1 Z{}      ;move to layer z height
G1 X{} Y{} ;move to starting position""".format(layer_curr, height[1], yx[0][0], yx[0][1]))
	for i in range(0,len(yx)-1):
		euclidian_dist += math.sqrt(pow(yx[i+1][0]-yx[i][0],2)+pow(yx[i+1][1]-yx[i][1],2))/1000
		print("G1 X{} Y{} E{}".format(yx[i][0], yx[i][1],
		(4*args.nozzle_dia*flow_mod_per*args.nozzle_dia*euclidian_dist)/(math.pi*pow(filament_dia/2,2))))
	print("G1 Z{}      ;move to traverse height".format(height[1] + clearence))

#print footer
print("""
M104 T0 S0      ;turn off extruder temp
M140 S0         ;turn off bed temp
M107            ;fan off
G0 Z{}         ;rapid move z to safe height
G28 XYZ         ;move all axis to home
;END OF FILE""".format(z_safe))