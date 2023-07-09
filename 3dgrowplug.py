#!/usr/local/bin/python3
# shebang for mac osx

"""
MODULE DESCRIPTION
Generates gcode for FDM 3D printers of a hydroponics/airoponics plant root grow plug
Cylander with solid walls and internal structure being a rectiliner grid made up of single filament strands
Prints single cylander on bed center
All print speeds and feeds are fixed at default bridging settings
G code head & foot based on Cura output for Ultimaker S5
Assumes bed- XYZ is greater than 200x200x200 by default

MODULE FEATURES
./3dgrowplug -cylander_dia 40 -z 40 --grid_space 1.75 --nozzel_dia 0.4 > out.g
"""

# import std lib
import sys
import argparse
import math

#get cmd line arguments
parser = argparse.ArgumentParser(prog='3dgrowplug',
  description='Generates gcode for FDM 3D printers of a hydroponics/airoponics plant root grow plug')
parser.add_argument('-d', '--cylander_dia', required=True,
                    help='diameter of cylander in mm')
parser.add_argument('-z', '--cylander_height', required=True,
                    help='z height of cylander in mm')
parser.add_argument('-g', '--grid_space', required=True,
                    help='internal grid spacing in mm')
parser.add_argument('-n', '--nozzel_dia', required=True,
                    help='nozzel diameter (and therefore layer height) in mm')
parser.add_argument('-b', '--bedXYZ', required=False,
                    help='bed length, width & height')

#validate arguments
args = parser.parse_args()
if args.b == None:
  args.b = 200
try:
    if type(args.b) != int and type(args.b) != float
      raise ValueError("bed XYZ must be a number")
    if type(args.n) != int and type(args.n) != float
      raise ValueError("nozzel diameter must be a number")  
    if args.n < 0 or args.n > 1:
      raise ValueError("nozzel diameter must be >0 <1")
    if type(args.d) != int and type(args.d) != float
      raise ValueError("cylander diameter must be a number")
    if args.d < 0 or args.d > args.b:
      raise ValueError("cylander diameter must be >0 <bed max")
    if type(args.z) != int and type(args.z) != float
      raise ValueError("cylander height must be a number")
    if args.z < 0 or args.z > args.b - 5 - args.n:
      raise ValueError("cylander height must be >0 <bed max - 5 - nozzel diameter")
    if type(args.g) != int and type(args.g) != float
      raise ValueError("grid spacing must be a number")
    if args.g < 0 or args.g > args.d:
      raise ValueError("grid spacing must be >0 <cylander diameter")
except ValueError as err:
  print(err)
  exit()
 
#setup other variables
args.z += args.z % args.n #add the remainder to z to ensure it is devisible by layer height without a remainder
z_safe = args.z + 5 #z safe height above work in mm
ccenter = args.b / 2
grid_count = math.trunc(args.d / args.g) + 1 #zero indexed
layer_count = args.z / args.n #number of layers
layer_curr = 0 #current layer
layer_heights = [] #list of z height for each layer
i = 1
while i <= layer_count:
  layer_heights.append(args.nozzel_dia * i)

#caculate cordinates
xy = []
xy.append((-abs(grid_count / 2 * args.g), sqrt(pow(arg.d/2, 2) - pow(xy[i][0]))) #start
for i in range(0, grid_count):
  xy.append((xy[i][0], -abs(sqrt(pow(arg.d/2, 2) - pow(xy[i][0]))))
  xy.append((xy[i][0] + args.g, xy[i][1]))
  xy.append((xy[i][0] + args.g, xy[i][1]))
  xy.append((xy[i][0], -abs(sqrt(pow(arg.d/2, 2) - pow(xy[i][0]))))
  xy.append((xy[i][0] + args.g, xy[i][1]))
  xy.append((xy[i][0] + args.g, xy[i][1]))

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
""").format(z_safe, ccenter, ccenter, xystart[0], xystart[1])

#1st layer
print("""
;LAYER:{}
G1 F600 Z{}      ;move to layer z height
G1 F2700 E0      ;ready extruder
G1 F600          ;set speed
G1 X{}
""").format(layer_curr, layer_height[0], xystart[0] + grid_ends)

for i in range(0, grid_count):
  print("G1 Y{} E{}").format(-abs(args.g))
layer_count += 1
layer_height *= layer_count

#nth layer
while layer_curr < layer_count:

#print footer
print("""
M104 T0 S0      ;turn off extruder temp
M140 S0         ;turn off bed temp
M107            ;fan off
G0 Z{d}         ;rapid move z to safe height
G1 F2700 E-6.5  ;move extruder back
G28 XYZ         ;move all axis to home
;END OF FILE
""").format(z_safe)