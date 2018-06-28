import os
import sys
import argparse
import re



class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


prsr = Parser()
prsr.add_argument("-o", "--output", action="store", dest="output", type=str, default='output.txt', help="Path to output file")
prsr.add_argument("-p", "--path", action="store", dest="path", type=str, help="path to logfile")

if len(sys.argv) == 1:
    prsr.print_help()
    sys.exit(1)

args = prsr.parse_args()

if __name__=='__main__':
    current_track = set()
    dict_to_sort = {}
    with open(args.path, 'rb') as f:
        for line in f.readlines():
            res = re.search('Track \d+', line.decode('utf-8'))
            if res and res.group(0) not in current_track:
                print(line.decode('utf-8'))
                current_track.add(res.group(0))
                dict_to_sort.update({re.search('Track \d+', res.group(0)).group(0):line})
            res = re.search('The result for Track \d+ was', line.decode('utf-8'))
            if res and res.group(0) not in current_track:
                print(line.decode('utf-8'))
                current_track.add(res.group(0))
                dict_to_sort.update({re.search('Track \d+', res.group(0)).group(0)+' result':line})
    for item in sorted(dict_to_sort.items()):
        res = re.search('\d+\:\d+\:\d+\.\d+', item[1].decode('utf-8'))
        if res:
            print(item[0]+' '+res.group(0))