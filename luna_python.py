##!/bin/python
from flask import Flask, request, abort, jsonify
#from flask.ext.cors import CORS
import base64
import datetime
from time import gmtime, strftime

app = Flask(__name__)
#cors = CORS(app)

replies = [
	{
		'status': 0,
		'message': u'OK',
	},
	{
		'status': 1,
		'message': u'Error',
	}
]

@app.route('/match', methods=['GET'])
def handle_get():
	return jsonify({'replies': replies})

@app.route('/', methods=['PUT'])
def handle_post():
	#print(request.data)
	handle_post.i += 1
	print(' ')
	if not request.json:
		print('Request is not JSon')
		abort(400)
	if 'data' in request.json and type(request.json['data']) != str:
		print('Error with data-field')
	else :
		print('Received data')

	if 'cadr' in request.json:
		print('cadr:')
	else :
		print('error with cadr-field')

	if 'identification' in request.json:
		print('identification:', request.json["identification"])
	else :
		print('error with identification-field')

	image = base64.b64decode(request.json['data'])
	#image1 = base64.b64decode(request.json['cadr'])
	fname = str(handle_post.i) + "_"+strftime("%Y-%m-%d_%H%M%S")+".jpg"
	#fname1 = str(handle_post.i) + "_10_@.jpg"
	
	with open(fname, "wb") as outfile:
		outfile.write(image)
	#with open(fname1, "wb") as outfile:
	#	outfile.write(image1)
	

	return jsonify({'reply': replies[0]})
handle_post.i = 0

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=6000, debug=True)

