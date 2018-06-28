import csv
import os

with open('images.csv', 'rb') as csvfile:
	file_reader = csv.reader(csvfile, delimiter=',')
	for row in file_reader:
		date_time = row[0]
		date_time_converted = date_time[:4]+date_time[5:7]+date_time[8:10]+date_time[11:13]+date_time[14:16]
		with open('images_converted2.csv','a+') as converted:
			converted.write(date_time_converted+','+row[1]+'\n')	
