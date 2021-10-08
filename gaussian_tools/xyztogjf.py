#!/usr/bin/env python3

# Author: Inigo Iribarren
# 01-12-2020

'''
##################
## Description: ##
##################

This script generates gaussian inputs from the selected xyz files.


############
## Usage: ##
############

    xyztogjf file 'commands for gaussian'

'''

# Imports
import sys

# Open XYZ file and read it

file = sys.argv[1]
name = file.split('.')[0]

commands = sys.argv[2]

logfile = open(file, 'r')
text = logfile.readlines()
logfile.close()

ofile = open(name+'.gjf', "w+")

ofile.write('%nproc=40\n')
ofile.write('%mem=150GB\n')
ofile.write('# $commands\n')
ofile.write('\n')
ofile.write(file+'\n')
ofile.write('\n')
ofile.write('1 1\n')
for i in text[2:]:
    ofile.write(''.join(i))
ofile.write('\n')
ofile.close()
