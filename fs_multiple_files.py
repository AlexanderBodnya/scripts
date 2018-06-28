import os
import subprocess

for file in os.listdir('/media/a.vysotina/Moskvarium/Videos'):
	path = '/media/a.vysotina/Moskvarium/Videos/'+file
	p = subprocess.Popen(['./FaceStream2', '--source', path,'--destination', 'http://0.0.0.0:6000'])
	p.wait()
	print('{} was processed!'.format(file))

