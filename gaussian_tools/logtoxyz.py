#!/usr/bin/env python3

# Author: Inigo Iribarren
# 26-03-2020

'''
##################
## Description: ##
##################

This script extracts the last structure from Gaussian log files a creates xyz
files with the coordinates.


############
## Usage: ##
############

If you want to convert all the files just run 
    log_extract
If you want to convert only those files containing a keyword:
    log_extract keyword

'''

# Imports
import glob
import sys
from my_functions import last_find, first_find


# Code for the elements 
code = {"1" : "H", "2" : "He", "3" : "Li", "4" : "Be", "5" : "B", \
"6"  : "C", "7"  : "N", "8"  : "O",  "9" : "F", "10" : "Ne", \
"11" : "Na" , "12" : "Mg" , "13" : "Al" , "14" : "Si" , "15" : "P", \
"16" : "S"  , "17" : "Cl" , "18" : "Ar" , "19" : "K"  , "20" : "Ca", \
"21" : "Sc" , "22" : "Ti" , "23" : "V"  , "24" : "Cr" , "25" : "Mn", \
"26" : "Fe" , "27" : "Co" , "28" : "Ni" , "29" : "Cu" , "30" : "Zn", \
"31" : "Ga" , "32" : "Ge" , "33" : "As" , "34" : "Se" , "35" : "Br", \
"36" : "Kr" , "37" : "Rb" , "38" : "Sr" , "39" : "Y"  , "40" : "Zr", \
"41" : "Nb" , "42" : "Mo" , "43" : "Tc" , "44" : "Ru" , "45" : "Rh", \
"46" : "Pd" , "47" : "Ag" , "48" : "Cd" , "49" : "In" , "50" : "Sn", \
"51" : "Sb" , "52" : "Te" , "53" : "I"  , "54" : "Xe" , "55" : "Cs", \
"56" : "Ba" , "57" : "La" , "58" : "Ce" , "59" : "Pr" , "60" : "Nd", \
"61" : "Pm" , "62" : "Sm" , "63" : "Eu" , "64" : "Gd" , "65" : "Tb", \
"66" : "Dy" , "67" : "Ho" , "68" : "Er" , "69" : "Tm" , "70" : "Yb", \
"71" : "Lu" , "72" : "Hf" , "73" : "Ta" , "74" : "W"  , "75" : "Re", \
"76" : "Os" , "77" : "Ir" , "78" : "Pt" , "79" : "Au" , "80" : "Hg", \
"81" : "Tl" , "82" : "Pb" , "83" : "Bi" , "84" : "Po" , "85" : "At", \
"86" : "Rn" , "87" : "Fr" , "88" : "Ra" , "89" : "Ac" , "90" : "Th", \
"91" : "Pa" , "92" : "U"  , "93" : "Np" , "94" : "Pu" , "95" : "Am", \
"96" : "Cm" , "97" : "Bk" , "98" : "Cf" , "99" : "Es" ,"100" : "Fm", \
"101": "Md" ,"102" : "No" ,"103" : "Lr" ,"104" : "Rf" ,"105" : "Db", \
"106": "Sg" ,"107" : "Bh" ,"108" : "Hs" ,"109" : "Mt" ,"110" : "Ds", \
"111": "Rg" ,"112" : "Uub","113" : "Uut","114" : "Uuq","115" : "Uup", \
"116": "Uuh","117" : "Uus","118" : "Uuo"}

# Select the files to convert. If we specify a keyword, it only takes those 
# containing the keyword

if len(sys.argv) == 2:
    files = glob.glob('*' + str(sys.argv[1]) + '*log')
else:
    files = glob.glob('*.log')


for file in files:
    # Load the text files:
    logfile = open(file, 'r')
    text = logfile.readlines()
    logfile.close()

    '''
    # Parameters
    nproc = text[first_find(text,"nproc")]
    mem = text[first_find(text,"mem=")]
    fun = text[first_find(text,"#")]

    #Charge and multiplicity
    charge = text[first_find(text,"Charge")].split()[2]
    mult = text[first_find(text,"Charge")].split()[5]
'''
    # Last coordinates:
    coord = text

    coord = coord[last_find(coord, 'Coordinates')+3:]
    coord = coord[:first_find(coord, '----')]

    # Translation of the atomic numbers to the atomic symbol and create the matrix with the coordinates
    m_coord = []
    for line in coord:
        column = line.split()
        symbol = code.get(column[1], 'X')

        m_coord.append([symbol, column[3], column[4], column[5]])

    # Output file:
    ofile = open(file.split('.')[0]+".xyz","w+") 

    ofile.write(str(len(coord))+"\n")
    ofile.write(file.split(".")[0]+"\n")
    for line in m_coord:
        ofile.write(str(line[0])+"\t"+str(line[1])+"\t"+str(line[2])+"\t"+str(line[3])+"\n")
    ofile.close()    


