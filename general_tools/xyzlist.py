#!/usr/bin/env python3
'''
Author: Inigo Iribarren
01-12-2020

Description:
This script reads all the conformers in an xyz file and separates them
in individual files

Usage:
    xyzlist.py file_name
'''

# Imports
import sys

# Open XYZ file and read it

file = sys.argv[1]
name = file.split('.')[0]

logfile = open(file, 'r')
text = logfile.readlines()
logfile.close()

# Extracting each conformation from the xyz file

line = 0
conf = 0

while line < len(text):
    coords = []
    
    # Extracting information
    n_atoms = int(text[line])
    title = text[line + 1]
    for i in range(0, n_atoms):
        coords.append([text[line + 2 + i ]])

    # Variables Update
    conf += 1
    line = line + 2 + n_atoms

    # Output writing
    name_conf = name + '_' + f"{conf:03d}"

    ofile = open(name_conf + '.xyz', "w+")

    ofile.write(str(n_atoms)+"\n")
    ofile.write(title)
    for i in coords:
        ofile.write(''.join(i))
    ofile.close()
