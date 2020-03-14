'''
Usage:
    python3 analysis.py -p [trace file path] -o [output file path]
'''

import re
import argparse
from collections import defaultdict

def analyze(args):
    with open(args.path, 'r') as fr:
        lines = fr.readlines()
    
    ins_table = defaultdict(lambda:0)
    data_table = defaultdict(lambda:0)
    I = L = S = M = 0
    print('Running')
    for line in lines:
        tmp = line.strip('\n').split(',')[0].split()
        tmp[1] = re.sub(r'^0*','',tmp[1])
        tmp[1] = ''.join(['0x', tmp[1][:-3], '000'])

        if tmp[0] == 'I':
            I += 1
        if tmp[0] == 'L':
            L += 1
        if tmp[0] == 'S':
            S += 1
        if tmp[0] == 'M':
            M += 1

        if tmp[0] == 'I':
            ins_table[tmp[1]] += 1
        else:
            data_table[tmp[1]] += 1
        
    with open(args.out, 'w') as fw:
        fw.write('Counts:\n')
        fw.write('  Instructions {}\n'.format(I))
        fw.write('  Loads        {}\n'.format(L))
        fw.write('  Stores       {}\n'.format(S))
        fw.write('  Modifies     {}\n'.format(M))
        fw.write('\n')
        fw.write('Instructions\n')
        [fw.write('{},{}\n'.format(ent, ins_table[ent])) for ent in ins_table]
        fw.write('Data\n')
        [fw.write('{},{}\n'.format(ent, data_table[ent])) for ent in data_table]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='path', default=None, help='Trace file path')
    parser.add_argument('-o', dest='out', default='./trace_analysis.txt', help='Output file path')
    args = parser.parse_args()
    analyze(args)