#!/usr/bin/env python3

"""
DESCRIPTION
g-code positive negative space swap
takes a g-code file exported by CAMBAM GRBL post-processor and swaps the
positive/negative symbols on the X and Y axis
as well as I J K axis used for arcs

INPUTS
path to g-code file

OUTPUTS
gcode valid for GRBL interpriter on stdout

USAGE
./gposneg.py ./in.gcode > out.gcode
"""

import re
import argparse
import sys
parser = argparse.ArgumentParser(description='swap g-code XY axis positive/negative symbols')
parser.add_argument('--g_in', '-f', type=str, required=True, help='path to input gcode file')
args = parser.parse_args()
v = vars(args)

#load file and print lines to stdout with XY signs changed
with open(args.g_in, 'r') as f:
	for line in f:
		strings = re.split(r'([^0-9|\.-])', line) #split at any non-numeric character
		strings = iter(strings)
		for string in strings:
			if  string == 'X' or string == 'x' or string == 'Y' or string == 'y' \
				or string == 'I' or string == 'i' or string == 'J' or string == 'j' \
				or string == 'K' or string == 'k':
				print(string, end='')
				num = next(strings)
				try:
					num = float(num)
				#if next string is not a number, just print it and move on
				except:
					print(num, end='')
				#swap sign if next string is a number
				else:
					print(float(num)*-1, end='')
			else:
				print(string, end='')
f.close()