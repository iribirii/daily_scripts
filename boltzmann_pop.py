#!/usr/bin/env python3

'''
Author: Inigo Iribarren
Date: 30-03-2020

Description:
This sctipt calculates the Bolztmann population of the selected files at a
selected temperature.

Usage:
    ee [-h] [-t TEMPERATURE] [-u UNITS] [-o] file

'''

# Import modules
import argparse
import glob
import sys
from sys import stderr
import numpy as np
import pandas as pd

# Personal module, in the same folder
import myfunctions as mf

class CpError(Exception):
    pass

# Variables
def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='ee',
        description='Automatically calculates the population of the selected molecules.'
    )
    parser.add_argument(
        'file',
        type=str,
        help='Keyword for files to submit without extension. If you want to calculate all of them put a .'
    )
    parser.add_argument(
        '-t',
        '--temperature',
        default=273.15,
        type=float,
        help='Temperature for calculating the population (default = 273.15)'
    )
    parser.add_argument(
        '-u',
        '--units',
        default='kcal',
        type=str,
        help='Units for calculating the population (default=kcal).\n Availabe options kcal and kJ (/mol).'
    )
    parser.add_argument(
        '-o',
        '--output',
        action='store_true',
        help='If used, saves a csv file with all the information.'
    )

    return parser.parse_args()

def main():
    args = cli()
    try:
        # Variables definition
        search = '*' + args.file + '*log'
        log_files = glob.glob(search)
        num_log_files = len(log_files)

        if args.units == 'kcal':
            r = 0.001985875
            units_converter = 627.5
        elif args.units == 'kj':
            r = 0.008314463
            units_converter = 2625.5

        t = args.temperature
        rt = r * t

        # This will track if any of the values do not appear
        is_scf = True
        is_G = True
        is_MP2 = True

        columns=['Name','State','SCFEnergy','MP2Energy','FreeEnergy']
        data = []
        
        log_files.sort()
        
        # Iterate all the files and extract the information
        
        for file in log_files:
        
            # Load the text files:
            logfile = open(file, 'r')
            text = logfile.readlines()
            logfile.close()
        
            # Calculate variables
        
            name = file.split(".")[0]
        
            try:
                scf = float(text[mf.last_find(text, 'SCF Done')].split()[4])
            except (IndexError, UnboundLocalError):
                is_scf = False
                scf = "?"
        
            try:
                G = float(text[mf.last_find(text, 'Sum of electronic and thermal Free Energies')].split()[7])
            except:
                is_G = False
                G = "?"
        
            try:
                mp2_raw =text[mf.last_find(text, 'EUMP2')].split()[5].split('D')
                mp2 = "{:.8f}".format(float(mp2_raw[0])*10**int(mp2_raw[1]))
            except (IndexError, UnboundLocalError):
                is_MP2 = False
                mp2 = "?"
        
            # Calculate state of the file
            end_text = text[-5:]
        
            try:
                end_text[mf.last_find(end_text, ' Normal termination')]
                state = 'OK'
            except:
                try:
                    end_text[mf.last_find(end_text, ' Error')]
                    state = 'ERR'
                except:
                    state = 'RUN'
        
        
            data.append([name, state, scf, mp2, G])
        
        
        
        dat_df = pd.DataFrame(data, columns=(columns))

        columns=['Name','State','SCFEnergy','MP2Energy','FreeEnergy']
        if not is_scf: 
            dat_df = dat_df.drop(['SCFEnergy'], axis=1)
        if not is_G: 
            dat_df = dat_df.drop(['FreeEnergy'], axis=1)
        if not is_MP2: 
            dat_df = dat_df.drop(['MP2Energy'], axis=1)
        
        if is_scf:
            ddSCF_name = 'ddE (' + args.units + '/mol)'
            dat_df[ddSCF_name] = (dat_df['SCFEnergy'] - dat_df['SCFEnergy'].min()) * units_converter
            dat_df['exp(ddE/RT)'] = np.exp(-dat_df[ddSCF_name]/rt)
            dat_df['% (electronic)'] = dat_df['exp(ddE/RT)'] / (dat_df['exp(ddE/RT)'].sum()) * 100
        
        if is_MP2:
            ddMP2_name = 'ddMP2 (' + args.units + '/mol)'
            dat_df[ddMP2_name] = (dat_df['MP2Energy'] - dat_df['MP2Energy'].min()) * units_converter
            dat_df['exp(ddMP2/RT)'] = np.exp(-dat_df[ddMP2_name]/rt)
            dat_df['% (MP2)'] = dat_df['exp(ddMP2/RT)'] / (dat_df['exp(ddMP2/RT)'].sum()) * 100
        
        if is_G:
            ddG_name = 'ddG (' + args.units + '/mol)'
            dat_df[ddG_name] = (dat_df['FreeEnergy'] - dat_df['FreeEnergy'].min()) * units_converter
            dat_df['exp(ddG/RT)'] = np.exp(-dat_df[ddG_name]/rt)
            dat_df['% (free)'] = dat_df['exp(ddG/RT)'] / (dat_df['exp(ddG/RT)'].sum()) * 100
        
        
        print('-----------------------------------------------------------------------------------')
        print('Temperature:\t' + str(t))
        print('-----------------------------------------------------------------------------------')
        print(dat_df)

        if args.output:
            output_name = 'boltzman_population_' + str(t) + 'K.csv' 
            dat_df.to_csv(output_name, index=False)
        
        
    except CpError as e:
        print(e, file=stderr)
        exit(1)


if __name__ == '__main__':
    main()



