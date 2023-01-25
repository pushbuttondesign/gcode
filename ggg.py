#!/usr/bin/env python3

"""
MODULE DESCRIPTION
g-code grid generator
generates valid grbl gcode for drawing grids with a cnc router
useful for 

MODULE FEATURES
saves out g-code file based on inputs
accepts X and Y maximum values to define rectangle
accepts pitch to define gap between lines
accepts one feed speed for all cutting passes
accepts only X and only Y for half grids
assumes XY start position will be set manually

USAGE
ggg.py -x 100 -y 100 -p 10 -f 3000 > out.gcode
"""

import argparse
parser = argparse.ArgumentParser(description='generate gcode for drawing grids')
parser.add_argument('--x-max', '-x', type=int, required=True, help='X working width in mm')
parser.add_argument('--y-max', '-y', type=int, required=True, help='Y working width in mm')
parser.add_argument('--pitch', '-p', type=int, required=True, help='Pitch between grid (stepover distance) in mm')
parser.add_argument('--feed', '-f', type=int, required=True, help='Horizontal feed in mm per minute')
parser.add_argument('--z-depth', '-z', type=float, default=0, help='Z depth to cut (0)')
parser.add_argument('--safe', '-s', type=float, default=5, help='Safe Z height (5)')
parser.add_argument('--only-x', default=False, action='store_true', help='Surface only in X (Default both)')
parser.add_argument('--only-y', default=False, action='store_true', help='Surface only in Y (Default both)')
args = parser.parse_args()
v = vars(args)

#g-code header
print('G54; Work Coordinates')
print('G21; mm mode')
print('G90; absolute positioning')
print('G28 z; home z axis')
print(';G28 x y; home x y at the same time - not used, assume set start positoin manually ')
print('G0 Z{}; rapid move to specified safe z height'.format(args.safe))
print('M3 S3000 $-1; start all spindles clockwise')
print('F{}; set feedrate'.format(args.feed))

#list x, y locations of  each row/column
pitch = args.pitch
def steps(end):
    s = [x for x in range(0, end, pitch)]
    #if end not a multiple of pitch then append end position
    if s[-1] != end:
        s.append(end)
    return s

x_steps = steps(args.x_max)
y_steps = steps(args.y_max)

#if odd number of steps, duplicate last value
if len(x_steps) % 2 != 0:
    x_steps.append(x_steps[-1])
if len(y_steps) % 2 != 0:
    y_steps.append(y_steps[-1])

#split into pairs
def pairs(steps):
    a = iter(steps)
    return zip(a, a)

x_steps = pairs(x_steps)
y_steps = pairs(y_steps)

#if y only mode false, cut x axis
if not args.only_y:
    print('')
    print('; X AXIS')
    print('G1 Z{} F500; slowly drop cutter into work piece'.format(args.z_depth))
    for a, b in y_steps:
        print('G1 Y{}'.format(a))
        print('G1 X{}'.format(args.x_max))
        print('G1 Y{}'.format(b))
        print('G1 X0')
    print('G0 Z{}; rapid lift cutter'.format(args.safe))
    print('G0 Y0; rapid reset y')

#if x only mode false, cut y axis
if not args.only_x:
    print('')
    print('; Y AXIS')
    print('G1 Z{} F500; slowly drop cutter into work piece'.format(args.z_depth))
    for a, b in x_steps:
        print('G1 X{}'.format(a))
        print('G1 Y{}'.format(args.y_max))
        print('G1 X{}'.format(b))
        print('G1 Y0')

#g-code footer
print('')
print('G28 z; home z axis')
print('M5 $-1; all spindles off')
print('G28 x y; home x y at the same time ')
print('M2; end program')
