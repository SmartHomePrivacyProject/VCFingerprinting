#python example to infer document vectors from trained doc2vec model
import gensim.models as g
import codecs
import cosine_similarity as cos
import csv, os, xlrd
import pandas



#load input data from xlsx file
def loaddata(filename,sheet):
	wb = xlrd.open_workbook(filename)
	data = wb.sheet_by_name(sheet)
	rows = data.nrows
	queries = data.col_values(0)
	return queries

def readcsv(filename):
	data = pandas.read_csv(filename)
	data.columns = ['query']
	return data
	
	
# store vectors in csv file
def write2file(filename,row):
	with open(filename,'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)
		

#parameters
#model="toy_data/model_yahoo.bin"
model="toy_data/model_yahoo_e150.bin"
print('model: ', model)


#*****load data from csv file
filename = 'filenamelist.csv'
data = readcsv(filename)
queries = data['query']
print(queries)
#print(len(queries)

#inference hyper-parameters
start_alpha=0.01
infer_epoch=1000

#load model
m = g.Doc2Vec.load(model)


#refresh .csv file
#before one round of infer,through the path, if .csv exit，then delet 
dir = os.path.abspath(os.path.join(os.path.dirname('__file__'),os.path.pardir))
output = 'vectors_queries_ya_e150_v300.csv'
items = os.listdir(dir)
vec = []
try:
	if output not in items:
		os.remove(output)
except IOError:
	print('refeshing csv file...')
finally:
	#infer test vectors and store
	for query in queries:
		vector = m.infer_vector(query,alpha=start_alpha,steps=infer_epoch)
		vec.append(vector)
		write2file(output,[query,vector,'\n#end\n'])
	
	


	 




