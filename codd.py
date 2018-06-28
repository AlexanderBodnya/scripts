import json
import requests
import argparse
from base64 import b64encode, b64decode
import os
import sys


def classify(photo_grz, photo_ts):
    url = "http://10.0.9.127:9999/classify"

    headers = {
        'content-type': 'application/json',
    }
    payload = {
        "photo_grz": photo_grz,
        "photo_ts": photo_ts,
        "classifiers": ['ts_bcd_type']
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    return response

class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    script_dir = os.getcwd()
    prsr = Parser()
    prsr.add_argument("-o", "--output", action="store", dest="output", type=str, default='output.txt',
                      help="Path to output file")
    prsr.add_argument("-p", "--path", action="store", dest="path", type=str,
                      help="path to dir with file to parse and rename")

    if len(sys.argv) == 1:
        prsr.print_help()
        sys.exit(1)

    args = prsr.parse_args()

    listing = os.listdir(args.path)
    os.chdir(args.path)
    for file in listing:
        with open(file, 'rb') as f:
            data = b64encode(f.read()).decode('utf-8')
            f.close()
        resp = classify(data, data)
        line = '{} {} {}'.format(file, resp['results'][0]['ts_type_ai'], resp['results'][0]['ts_type_ai_score'])
        with open(script_dir+'\\'+args.output, 'a', encoding='utf-8') as f:
            f.write(line+'\n')
            f.close()



