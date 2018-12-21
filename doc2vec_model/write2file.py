import csv

def write2file(filename,row):
	with open(filename,'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)
		

