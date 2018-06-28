import os
import requests
import sys
from multiprocessing import Pool
import argparse



params = {'estimate_attributes': '1'}
resulting_table = []

class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

prsr = Parser()


prsr.add_argument("-dp", "--dir-path", action = "store", dest = "path", type = str, help = "option to define the path to the directory with photos for extraction")
prsr.add_argument("-url", "--url-46-CNN", action = "store", dest = "url", type = str, default='https://luna2api.faceis.ru/2/storage/descriptors', help = "URL interface for extraction")
prsr.add_argument("-xt", "--x-auth-token", action = "store", dest = "token", type = str, default='65be3f50-a773-4845-8597-856f8a16d991', help = "Authentification token")
prsr.add_argument("-ct", "--content-type", action = "store", dest = "content", type = str, default='image/jpeg', help = "Content type")
prsr.add_argument("-t", "--threads", action = "store", dest = "threads_num", type = int, default='4', help = "Thread count(def=4)")
prsr.add_argument("-o", "--output", action = "store", dest = "output", type = str, default='output.txt', help = "Path to output file")

if len(sys.argv) == 1:
    prsr.print_help()
    sys.exit(1)
    
args = prsr.parse_args()

url46CNN = args.url
headers1 = {'Content-type': args.content,
            'X-Auth-Token': args.token}


def api_request(file):
    with open(file, 'rb') as image:
        result = []
        read_image = image.read()
        try:
            response = requests.post(url46CNN, headers=headers1, params=params, data=read_image).json()
            if float(response['faces'][0]['attributes']['gender']) > 0.5:
                result = ('{}; age {}; gender Male'.format(file, int(response['faces'][0]['attributes']['age'])))
            else:
                result = ('{}; age {}; gender Female'.format(file, int(response['faces'][0]['attributes']['age'])))
        except:
            result = ('File {} no faces found'.format(file))
    
    return result
    
if __name__ == '__main__':
    cwd = os.getcwd()
    data_folder = os.path.abspath(args.path)
    os.chdir(data_folder)
    filelist_sorted = []
    number = ''
    for file in sorted(os.listdir(data_folder)):
        if file[:5] != number:
            filelist_sorted.append(file)
            number = file[:5]
        else:
            continue
    print('{} elements to extract!'.format(len(filelist_sorted)))
    with Pool(args.threads_num) as pool:
        resulting_table.append(pool.map(api_request, filelist_sorted))
        pool.close()
        pool.join()
    os.chdir(cwd)
	
with open(args.output, 'a') as output:
    for table in resulting_table:
        for line in table:
            output.write(line+'\n')
            