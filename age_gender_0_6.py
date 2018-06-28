import os
import requests
import sys
from multiprocessing import Pool
import argparse
import subprocess



params = {'estimate_attributes': '1'}
resulting_table = []

class Parser(argparse.ArgumentParser):
	def error(self, message):
		sys.stderr.write('error: %s\n' % message)
		self.print_help()
		sys.exit(2)

prsr = Parser()

file_names = prsr.add_mutually_exclusive_group()
file_names.add_argument("-dp", "--dir-path", action = "store", dest = "path", help = "option to define the path to the directory with photos for extraction")
file_names.add_argument("-p", "--path", action = "store", dest = "txt_path", help = "option to define the path to the txt with file-paths of photos to be extracted")
prsr.add_argument("-url", "--url-46-CNN", action = "store", dest = "url", type = str, default='https://luna2api.faceis.ru/2/storage/descriptors', help = "URL interface for extraction")
prsr.add_argument("-xt", "--x-auth-token", action = "store", dest = "token", type = str, default='65be3f50-a773-4845-8597-856f8a16d991', help = "Authentification token")
prsr.add_argument("-ct", "--content-type", action = "store", dest = "content", type = str, default='image/jpeg', help = "Content type")
prsr.add_argument("-t", "--threads", action = "store", dest = "threads_num", type = int, default='4', help = "Thread count(def=4)")
prsr.add_argument("-o", "--output", action = "store", dest = "output", type = str, default='output.txt', help = "Path to output file")
prsr.add_argument("-nu", "--not-uniq", action = "store_false", dest = "uniq", help = "Use this flag to process all photos, ignoring person ID")


if len(sys.argv) == 1:
	prsr.print_help()
	sys.exit(1)
	
args = prsr.parse_args()

url46CNN = args.url
headers1 = {'Content-type': args.content,
			'X-Auth-Token': args.token}


def api_request(file):
	try:
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
	except:
		return 'Not a valid file!'

	return result
	
if __name__ == '__main__':

	start_path = os.getcwd()
	filelist_sorted = []
	filelist = []
	number = ''

	if args.path == None:
		with open(args.txt_path) as file:
			filelist = [line.strip() for line in file]
	else:
		# try:
		# 	filelist = os.listdir(args.path)
		# 	print(filelist)
		# except:
			cmd = 'find '+args.path
			process = subprocess.Popen(cmd, shell=True,
			stdout=subprocess.PIPE, 
			stderr=subprocess.PIPE)
			# wait for the process to terminate
			out, err = process.communicate()
			errcode = process.returncode
			for element in out.split():
				print(element)
				filelist.append(element.decode('utf-8'))
	if args.uniq == True:
		for file in sorted(filelist):
			if file[:5] != number:
				filelist_sorted.append(file)
				number = file[:5]
			else:
				continue
		print('{} uniq elements to extract!\n'.format(len(filelist_sorted)))
		with Pool(args.threads_num) as pool:
			resulting_table.append(pool.map(api_request, filelist_sorted))

	elif args.uniq == False:
		for file in sorted(filelist):
		   filelist_sorted.append(file)
		print('{} elements to extract!\n'.format(len(filelist_sorted)))
		print(filelist_sorted)
		with Pool(args.threads_num) as pool:
			resulting_table.append(pool.map(api_request, filelist_sorted))

	with open(start_path+'/'+args.output, 'a') as output:
		for line in resulting_table[0]:
			output.write(line+'\n')
