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
ggg.py -x -100 -y 100 --x-pitch -10 --y-pitch 10 -f 500 -z -10 --only-y > out.gcode
"""

import argparse
parser = argparse.ArgumentParser(description='generate gcode for drawing grids')
parser.add_argument('--x-max', '-x', type=int, required=True, help='X working width in mm')
parser.add_argument('--y-max', '-y', type=int, required=True, help='Y working width in mm')
parser.add_argument('--x-pitch', '-a', type=int, required=True, help='pitch between grid (stepover distance) in mm')
parser.add_argument('--y-pitch', '-b', type=int, required=True, help='pitch between grid (stepover distance) in mm')
parser.add_argument('--feed', '-f', type=int, required=True, help='horizontal feed in mm per minute')
parser.add_argument('--z-depth', '-z', type=float, default=0, help='Z depth to cut (default 0 for air cut)')
parser.add_argument('--only-x', default=False, action='store_true', help='surface only in X (default both)')
parser.add_argument('--only-y', default=False, action='store_true', help='surface only in Y (default both)')
args = parser.parse_args()
v = vars(args)

#argument validation
if args.x_pitch * args.x_max * args.y_max * args.feed == 0:
    raise ValueError('Input values must be non-zero numbers0')
if args.x_max < 0 and args.x_pitch >= 0 or args.x_max >=0 and args.x_pitch < 0:
    raise ValueError('Both axis max & pitch must have the same sign')
if args.y_max < 0 and args.y_pitch >= 0 or args.y_max >=0 and args.y_pitch < 0:
    raise ValueError('Both axis max & pitch must have the same sign')
if args.feed < 500 or args.feed > 1500:
    print("Are you sure a feed rate of {} mm per minute is correct?".format(args.feed))
    input('press any key to continue')
if args.z_depth > 80:
    print("Are you sure a Z depth of {} mm is correct?".format(args.z_depth))
    input('press any key to continue')

#g-code header
print('; HEADER')
print('; AUTHOR: export from ggg.py')
print('; PART #: grid-01-01')
print('G54; Work Coordinates')
print('G21; mm mode')
print('G90; absolute positioning')
print('G28 z; home z axis')
print(';G28 x y; home x y at the same time - not used, assume set start position manually ')
print('M3 S3000 $-1; start all spindles clockwise')
print('F{}; set feedrate'.format(args.feed))

#return list of cordinates between 0 and end by pitch
def steps(end, pitch):
    s = [x for x in range(0, end, pitch)]
    #if end not a multiple of pitch then append end position
    if s[-1] != end:
        s.append(end)
    return s

x_steps = steps(args.x_max, args.x_pitch)
y_steps = steps(args.y_max, args.y_pitch)

#if odd number of steps, append None
if len(x_steps) % 2 != 0:
    x_steps.append(None)
if len(y_steps) % 2 != 0:
    y_steps.append(None)

#split into pairs
def pairs(steps):
    a = iter(steps)
    return zip(a, a)

x_pairs = pairs(x_steps)
x_reverse = pairs(reversed(x_steps))
y_pairs = pairs(y_steps)

#keep track of positions
x_cur = 0
y_cur = 0

print('G1 Z{} F200; slowly drop cutter to final cut depth'.format(args.z_depth))

if args.only_y == False:
    print('')
    print('; X AXIS')
    for a, b in y_pairs:
        if b != None:
            print('G1 Y{}'.format(a))
            print('G1 X{}'.format(args.x_max))
            print('G1 Y{}'.format(b))
            print('G1 X0')
            #save ending positions
            y_cur = b
            x_cur = 0
        else:
            print('G1 Y{}'.format(a))
            print('G1 X{}'.format(args.x_max))
            #save ending positions
            y_cur = a
            x_cur = args.x_max

if args.only_x == False:
    print('')
    print('; Y AXIS')
    #if starting at X0 Y0 as y only mode is active
    if x_cur == 0 and y_cur == 0:
        for a, b in x_pairs:
            if b != None:
                print('G1 X{}'.format(a))
                print('G1 Y{}'.format(args.y_max))
                print('G1 X{}'.format(b))
                print('G1 Y0')
            else:
                print('G1 X{}'.format(a))
                print('G1 Y{}'.format(args.y_max))
    #if starting at X0 YMAX
    elif x_cur == 0:
        for a, b in x_pairs:
            if b != None:
                print('G1 X{}'.format(a))
                print('G1 Y0')
                print('G1 X{}'.format(b))
                print('G1 Y{}'.format(args.y_max))
            else:
                print('G1 X{}'.format(a))
                print('G1 Y0')
    #if starting at XMAX YMAX
    else:
        for a, b in x_reverse:
            if a != None:
                print('G1 Y0')
                print('G1 X{}'.format(a))
                print('G1 Y{}'.format(args.y_max))
                print('G1 X{}'.format(b))
            else:
                print('G1 Y0')
                print('G1 X{}'.format(b))

#g-code footer
print('')
print('; FOOTER')
print('G28 z; home z axis')
print('M5 $-1; all spindles off')
print('G28 x y; home x y at the same time ')
print('M2; end program')
