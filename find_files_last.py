import os
import argparse
import sys
import shutil
import re


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    script_dir = os.getcwd()
    prsr = Parser()
    prsr.add_argument("-o", "--output", action="store", dest="output", type=str,
                      help="Path to output file")
    prsr.add_argument("-p", "--path", action="store", dest="path", type=str,
                      help="path to dir with file to parse and rename")
    prsr.add_argument("-l", "--list", action="store", dest="list", type=str,
                      help="path to dir with file to parse and rename")

    if len(sys.argv) == 1:
        prsr.print_help()
        sys.exit(1)

    args = prsr.parse_args()
    list_of_files = []
    list_of_needed = []
    counter = 0
    counter2 = 0
    with open(args.list, 'r') as f:
        lines = f.readlines()
        for line in lines:
            list_of_needed.append(line.strip('\n'))

    list_of_needed = set(list_of_needed)

    for root, dirs, files in os.walk(args.path):
        for filename in files:
            res = re.search('\d+', filename)
            if res and res.group(0) in list_of_needed:
                list_of_files.append(os.path.join(args.path, filename))
                counter += 1
                print('Occurrence found! Current count is {}!'.format(counter))
                list_of_needed.remove(res.group(0))
            else:
                counter2 += 1
                print('Skipping.. Currently {} files skipped!'.format(counter2))

    for item in list_of_needed:
            print(item)
