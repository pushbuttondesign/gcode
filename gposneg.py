#!/usr/bin/env python3

"""
DESCRIPTION
g-code positive negative space swap
takes a g-code file exported by CAMBAM GRBL post-processor and swaps the
positive/negative symbols on the X and Y axis as required
I is swapped with X, J is swapped with Y for arcs

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
parser.add_argument('--swap', '-s', type=str, required=True, help='xy to swap both axis, or select one')
args = parser.parse_args()

#load file and print lines to stdout with XY signs changed
with open(args.g_in, 'r') as f:
	for line in f:
		
		#skip line if comment
		if line[0] == '(' or line[0] == '#':
			print(line, end='')
		
		else:
			strings = re.split(r'([^0-9|\.-])', line)
			#split at any non-numeric character
			
			skip = 0
			for i in range(0, len(strings)):
				
				if skip == 1:
					skip = 0
					continue

				string = strings[i]
				
				#if string is last in line, print and break
				try:
					num = strings[i+1]
				except:
					print(string, end='')
					break
				
				#if string is x axis
				if  string == 'X' or string == 'x' or string == 'I' or string == 'i':	
					
					print(string, end='') #print x
					
					#is next string a number
					try:
						num = float(num)
						#swap sign and print if flagged
						if 'x' in args.swap:
							print(float(num)*-1, end='')
							skip = 1
							
					#if next string is not a number, skip
					except:
						pass
					
				#if string is y axis
				elif   string == 'Y' or string == 'y' or string == 'J' or string == 'j':
					
					print(string, end='') #print y
					
					#is next string a number
					try:
						num = float(num)
						#swap sign and print if flagged
						if 'y' in args.swap:
							print(float(num)*-1, end='')
							skip = 1
							
					#if next string is not a number, skip
					except:
						pass
					
				else:
					print(string, end='')
				i += 1
f.close()
