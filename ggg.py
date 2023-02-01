#!/usr/bin/env python3

"""
DESCRIPTION
g-code grid generator
generates valid grbl gcode for drawing grids with a cnc router
useful for surfacing and engraving measuring grids

INPUTS
X and Y maximum values to define rectangle
different pitches to define gap between cuts in X and Y
feed speed for all G1 cuts
Z value for cutting depth, default is manually set cut
option for only X and only Y for lines in one axis only
option for air traverse between grid lines or cutting them
safe Z value for traversing

USAGE
./ggg.py -x -100 -y 100 --x-pitch -10 --y-pitch 10 -f 500 -z -10 --only-y --air-traverse > sample.gcode
"""

import argparse
parser = argparse.ArgumentParser(description='generate gcode for drawing grids')
parser.add_argument('--x-max', '-x', type=int, required=True, help='X working width in mm')
parser.add_argument('--y-max', '-y', type=int, required=True, help='Y working width in mm')
parser.add_argument('--x-pitch', '-a', type=int, required=True, help='pitch between grid (stepover distance) in mm')
parser.add_argument('--y-pitch', '-b', type=int, required=True, help='pitch between grid (stepover distance) in mm')
parser.add_argument('--feed', '-f', type=int, required=True, help='horizontal feed in mm per minute')
parser.add_argument('--z-depth', '-z', type=float, default=0, help='Z depth to cut (default 0)')
parser.add_argument('--only-x', default=False, action='store_true', help='surface only in X (default both)')
parser.add_argument('--only-y', default=False, action='store_true', help='surface only in Y (default both)')
parser.add_argument('--air-traverse', default=False, action='store_true', help='raises cutter when traversing (default cuts traverses)')
parser.add_argument('--z-safe', '-s', type=float, default=0, help='safe Z height for traversing (default 0 for home position)')
args = parser.parse_args()
v = vars(args)

#argument validation
if args.x_pitch * args.x_max * args.y_max * args.feed == 0:
    raise ValueError('XY & feed input values must be non-zero numbers0')
if args.x_max < 0 and args.x_pitch >= 0 or args.x_max >=0 and args.x_pitch < 0:
    raise ValueError('Both axis max & pitch must have the same sign')
if args.y_max < 0 and args.y_pitch >= 0 or args.y_max >=0 and args.y_pitch < 0:
    raise ValueError('Both axis max & pitch must have the same sign')
#if args.feed < 500 or args.feed > 1500:
    #TODO: current usage redirects stdout, swap to python file manupulation to present errors
    #print("Are you sure a feed rate of {} mm per minute is correct?".format(args.feed), flush=True)
    #input("press any key to continue")
#if args.z_depth < -90:
    #print("Are you sure a Z depth of {} mm is correct?".format(args.z_depth), flush=True)
    #input("press any key to continue")

#g-code header
print('; HEADER')
print('; AUTHOR: export from ggg.py')
print('; PART #: grid-01-01')
print('G54; work Coordinates')
print('G21; mm mode')
print('G90; absolute positioning')
print('G28 Z0; home z axis')
print('G28 X0 Y0; home x y at the same time')
print('M3 S3000; start default spindle 0 clockwise at given RPM')

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

if args.only_y == False:
    print('')
    print('; X AXIS')
    print('G1 Z{} F200; cutting depth'.format(args.z_depth))
    #assume starting at X0 Y0
    for a, b in y_pairs:
        if b != None:
            print('G1 Y{} F{}'.format(a, args.feed))
            if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
            print('G1 X{} F{}'.format(args.x_max, args.feed))
            if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
            print('G1 Y{} F{}'.format(b, args.feed))
            if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
            print('G1 X0 F{}'.format(args.feed))
            if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
            #save ending positions
            y_cur = b
            x_cur = 0
        else:
            print('G1 Y{} F{}'.format(a, args.feed))
            if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
            print('G1 X{} F{}'.format(args.x_max, args.feed))
            if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
            #save ending positions
            y_cur = a
            x_cur = args.x_max

if args.only_x == False:
    print('')
    print('; Y AXIS')
    print('G1 Z{} F200; cutting depth'.format(args.z_depth))
    #if starting at X0 Y0 as y only mode is active
    if x_cur == 0 and y_cur == 0:
        for a, b in x_pairs:
            if b != None:
                print('G1 X{} F{}'.format(a, args.feed))
                if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
                print('G1 Y{} F{}'.format(args.y_max, args.feed))
                if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
                print('G1 X{} F{}'.format(b, args.feed))
                if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
                print('G1 Y0 F{}'.format(args.feed))
                if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
            else:
                print('G1 X{} F{}'.format(a, args.feed))
                if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
                print('G1 Y{} F{}'.format(args.y_max, args.feed))
                if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
    #if starting at X0 YMAX
    elif x_cur == 0:
        for a, b in x_pairs:
            if b != None:
                print('G1 X{} F{}'.format(a, args.feed))
                if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
                print('G1 Y0 F{}'.format(args.feed))
                if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
                print('G1 X{} F{}'.format(b, args.feed))
                if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
                print('G1 Y{} F{}'.format(args.y_max, args.feed))
                if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
            else:
                print('G1 X{} F{}'.format(a, args.feed))
                if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
                print('G1 Y0 F{}'.format(args.feed))
                if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
    #if starting at XMAX YMAX
    else:
        for a, b in x_reverse:
            if a != None:
                print('G1 Y0 F{}'.format(args.feed))
                if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
                print('G1 X{} F{}'.format(a, args.feed))
                if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
                print('G1 Y{} F{}'.format(args.y_max, args.feed))
                if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
                print('G1 X{} F{}'.format(b, args.feed))
                if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))
            else:
                print('G1 Y0 F{}'.format(args.feed))
                if args.air_traverse == True: print('G1 Z{} F200'.format(args.z_depth))
                print('G1 X{} F{}'.format(b, args.feed))
                if args.air_traverse == True: print('G0 Z{}'.format(args.z_safe))

#g-code footer
print('')
print('; FOOTER')
print('G28 Z0; home z axis')
print('M5; stop default spindle 0')
print('G28 X0 Y0; home x y at the same time ')
print('M2; end program')
