import os
import requests
import sys
from multiprocessing import Pool
import argparse
import subprocess
import glob


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


prsr = Parser()
prsr.add_argument("-o", "--output", action="store", dest="output", type=str, default='output.txt', help="Path to output file")
prsr.add_argument("-p", "--path", action="store", dest="path", type=str, help="path to dir with file to parse and rename")

if len(sys.argv) == 1:
    prsr.print_help()
    sys.exit(1)

args = prsr.parse_args()

listing = os.listdir(args.path)
print('There are {} files to rename!'.format(len(listing)))
os.chdir(args.path)
for file1 in listing:
    filename = file1.split('(')
    try:
        filename2 = filename[1].split(')')

    except IndexError:
        print('IndexErr!')


