import config
import re
import os, sys
import numpy as np
import pandas as pd

'''
Counte the number of ligands in a file
Counte the number of the atoms in a ligand
'''


def count_liangd_num(input_file):
    '''
    count the number of ligands for given ligands in mol2 foramt.

    :param input_file: path of input file eg. '/n/scratch2/xl198/data/source/ligands/1a2b/1a2b_1234_liagnd.mol2'
    :return:  [filename,atom_num] eg [1a2b_1234_liagnd,10]
    '''

    # count the number of the single ligand in one file
    ligand_count = 0
    with open(input_file) as input:
        for line in input:
            if line == '@<TRIPOS>MOLECULE\n':
                ligand_count += 1

    return [os.path.basename(input_file), ligand_count]


def count_atom_num(input_file):
    '''
    count the number of atoms for given ligand in mol2 foramt.

    :param input_file: path of input file eg. '/n/scratch2/xl198/data/source/ligands/1a2b/1a2b_1234_liagnd.mol2'
    :return: [ID,atom_num] eg [1a2b_1234,10]
    '''

    # count the number of the atoms in ligand
    flag = False
    atom_num = 0
    with open(input_file) as input:
        for line in input:
            if not flag and line == '@<TRIPOS>ATOM\n':
                flag = True
            elif line == '@<TRIPOS>BOND\n':
                break
            elif flag:
                atom_num += 1

    name = os.path.basename(input_file)
    ID = '_'.join(name.split('_')[:2])

    return [ID, atom_num]


def read_file_path(input_path):
    '''
    Get the path of file used as input of count function
    :param input_path:
    :return:
    '''

    for dirname, dirnames, filenames in os.walk(input_path):
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            yield file_path


def count_and_report(input_path, report, counter):
    pathes = read_file_path(input_path)
    result = [counter(path) for path in pathes]
    df = pd.DataFrame(data=result, columns=['file', 'atom_num'])
    df.to_csv(report, index=False)




def example():

    # count atom num for every ligand in input_path
    count_and_report("/n/scratch2/yw174/result/fast",
                     os.path.join('/home/xl198/report', 'atom_count.csv'),
                     count_atom_num)

    # count number of ligands in every file in input_path
    count_and_report('/n/scratch2/xl198/data/fast',
                     os.path.join('/home/xl198/report','ligand_num.csv'),
                    count_liangd_num)



if __name__ == '__main__':
    main()
