
with open('tweet.txt') as inf:
	long = []
	lati = []
	for line in inf:
        	parts = line.split("|")
        	if len(parts) > 3:   
            		num = parts[3].split(",")
			long.append(num[0])
			lati.append(num[1])
#print num[1]


import xlwt
file = xlwt.Workbook()
table = file.add_sheet('address',cell_overwrite_ok=True)

import time
from pygeocoder import Geocoder
for i in range(2483,5001):
	try:
		results = Geocoder.reverse_geocode(float(lati[i]), float(long[i]))
		print(results[0])
		table.write(i,0,str(results[0]))
	except:
		table.write(i,0,str(" "))
	time.sleep(0.11)

file.save('add.xls')
