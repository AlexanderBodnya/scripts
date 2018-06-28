import os
import requests
import sys
from multiprocessing import Pool
import argparse
import subprocess
import glob

params = {'estimate_quality': '1'}
resulting_table = []


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


prsr = Parser()

file_names = prsr.add_mutually_exclusive_group()
file_names.add_argument("-dp", "--dir-path", action="store", dest="path",
                        help="option to define the path to the directory with photos for extraction")
prsr.add_argument("-url", "--url-46-CNN", action="store", dest="url", type=str,
                  default='http://10.0.9.65:5000/3/storage/descriptors', help="URL interface for extraction")
prsr.add_argument("-xt", "--x-auth-token", action="store", dest="token", type=str,
                  default='5c8ec6e2-5237-4062-a2e9-5a6a5a5fd089', help="Authentification token")
prsr.add_argument("-ct", "--content-type", action="store", dest="content", type=str, default='image/jpeg',
                  help="Content type")
prsr.add_argument("-t", "--threads", action="store", dest="threads_num", type=int, default='4',
                  help="Thread count(def=4)")
prsr.add_argument("-o", "--output", action="store", dest="output", type=str, default='output.txt',
                  help="Path to output file")

if len(sys.argv) == 1:
    prsr.print_help()
    sys.exit(1)

args = prsr.parse_args()

url46CNN = args.url
headers1 = {'Content-type': args.content,
            'X-Auth-Token': args.token}


def api_request(file):
    with open(file, 'rb') as image:
        read_image = image.read()
        try:
            response = requests.post(url46CNN, headers=headers1, params=params, data=read_image).json()
            result = (
                '{}, quality_light: {}, quality_dark: {}, quality_saturation: {}, quality_blurriness: {}, quality_score: {}, height: {}, width: {}'.format(
                    file,
                    response['faces'][0]['quality']['light'],
                    response['faces'][0]['quality']['dark'],
                    response['faces'][0]['quality']['saturation'],
                    response['faces'][0]['quality']['blurriness'],
                    response['faces'][0]['score'],
                    response['faces'][0]['rect']['height'],
                    response['faces'][0]['rect']['width']
                ))
        except KeyError:
            result = ('{}, error code: {}, detail: {}'.format(
                file,
                response['error_code'],
                response['detail'],
            ))
        except:
            result = 'Unknown exception during API request!'

    return result


if __name__ == '__main__':
    current_dir = os.getcwd()
    filelist = glob.glob(os.path.abspath(args.path) + '/*.*')
    for file in filelist:
        result = api_request(file)
        
        with open(args.output,'a') as f:
            f.write(result+'\n')
