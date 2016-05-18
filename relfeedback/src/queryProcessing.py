"""
Author: Bijal Parikh
"""
import parseHtml as ph
import stopliststemmer as ss
import snowballstemmer as sst
from searchUtility import * 
import time

orig = vectorSpaceModel.populateMatrix()
currCache = Cache(orig,vectorSpaceModel.matrix_new,ii.readFromFiles(),vectorSpaceModel.idf_list)

def process_docid(doc_id_list):
	mapping = dict()
	#print("Doc Ids inside query processing")
	#print(doc_id_list)
	f = open("/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/InvertedIndex/etc/mapping.txt",'r')
	for line in f.readlines():
		temp = line.split(" ")
		mapping[temp[0]] = temp[1].rstrip()
	file_name_list = list()
	#print("File names in output")
	count = 0;
	for id in doc_id_list:
		count += 1
		#print(count)
		#print(mapping[str(id)])
		file_name_list.append(mapping[str(id)])
		tempname = mapping[str(id)]
	return file_name_list

def processQuery(qry):
	time1 = time.time()
	#Step 1 is to remove any punctuation
	qry = ph.remove_pattern('(?s)<!.*?(/>|<-->)',qry)
	#Step 2 is to loop over remaining words , remove stop words, stem words and compute a list of words and their term frequency 
	stopWords = ss.getStopWords()
	stemmer = sst.EnglishStemmer()
	list_of_words = qry.split()
	#print(list_of_words)
	query_tf_dict = dict()
	for word in list_of_words:
		tmpWord = word.rstrip().lower()
		if tmpWord not in stopWords:
			stemmedWord =stemmer.stemWord(tmpWord)
			if query_tf_dict.has_key(stemmedWord):
				count = query_tf_dict[stemmedWord] + 1
			else:
				count = 1
			query_tf_dict[stemmedWord] = count
	#Step 3 is to send the query to vector space model and expect a list of docIds
	#Update code from prabha here
	out = performSearch(query_tf_dict,currCache,qry);
	doc_list = out[0]
	similarity_map = out[1]
	file_details = process_docid(doc_list)
	sim_list = [0]*len(doc_list)
	i = 0
	for id in doc_list:
		sim_list[i] = str((similarity_map[id]))
		i += 1
	difference = time.time() - time1
	return (file_details,sim_list,difference)

def processQueryRelFeed(doc_list,qry):
	time1 = time.time()
	#First step is to get the doc numbers corresponding to file name
	#Reverse mapping lookup
	#print("I am reaching here")
	#print(qry)	
	num_list = list()
	mapping = dict()
	f = open("/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/InvertedIndex/etc/rev_mapping.txt",'r')
	for line in f.readlines():
		temp = line.split(" ")
		mapping[temp[0].rstrip()] = temp[1].rstrip()
	for name in doc_list:
		#print(name)
		num_list.append(mapping[name])
	out = performRelevanceFeedback(qry,num_list,currCache)
	docList = out[0]
	similarity_map = out[1]
	file_details = process_docid(docList)
	sim_list = [0]*len(docList)
	i = 0
	for id in docList:
		sim_list[i] = str((similarity_map[id]))
		i += 1
	difference = time.time() - time1
	return (file_details,sim_list,difference)