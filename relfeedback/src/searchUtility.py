import math
import snowballstemmer
import vectorSpaceModel
import stopliststemmer as ss
import invertedIndex as ii
from InvertedIndexNode import InvertedIndexNode
from PostingListNode import PostingListNode
from cache import *
from queryDetails import *

similarity_map = dict()
similarity_map_sorted = dict()
query_cache = dict()
vocab_size = ss.readVocabSize()
relfeed_cache = dict()

def performRelevanceFeedback(query_string, docIdList,currCache):
	print("In relevance feedback")
	docLength = len(docIdList)
	print("Doc id length")
	#print(docLength)
	qryDetails = relfeed_cache[query_string]
	qry_vector = qryDetails.query_vector
	orig_search_result = qryDetails.search_result
	negDocs = list()
	for id in orig_search_result:
		if id not in docIdList:
			negDocs.append(id)
	print("Size of negDocs")
	#print(len(negDocs))
	matrix = currCache.original_matrix
	result = [0] * vocab_size
	#print qry_vector
	sum_doc_vector = [0]*vocab_size
	diff_doc_vector =[0]*vocab_size 
	#population sum of doc vectors
	for docId in docIdList:
		for i in range(vocab_size):
			sum_doc_vector[i] += matrix[i][int(docId) - 1]
		
	for docId in negDocs:
		for i in range(vocab_size):
			diff_doc_vector[i] += matrix[i][int(docId) - 1]

	#print(sum_doc_vector)
	#divide by length of docId
	beta = 0.5
	gamma = 0.3
	magnitude = 0.0
	#print("beta")
	#print(sum_doc_vector[12679])
	#print(qry_vector[12679])
	#print(beta * (sum_doc_vector[12679]//docLength))
	#print(beta * (sum_doc_vector[12679]/docLength))
	#print(float(beta * (sum_doc_vector[12679]//docLength)))
	#print(float(beta * (sum_doc_vector[12679]/docLength)))
	nDocLength = len(negDocs)
	for i in range(vocab_size):
		result[i] = qry_vector[i] + (beta * (sum_doc_vector[i])/docLength) - (gamma * (diff_doc_vector[i])/nDocLength)
		magnitude = magnitude + math.pow(result[i],2)
	magnitude = round(math.sqrt(magnitude),3)
	#construct position_map
	norm_qry_vector = calculateNQVector(qryDetails.qlist,magnitude,qryDetails.positionMap,result)
	sim_map = calculateSimilarity(qryDetails.search_result,norm_qry_vector,currCache.norm_matrix)
	fin_list = documentRanking(len(qryDetails.search_result),sim_map)
	return (fin_list,sim_map)

def binary_search(ds_list, key, candidate_document):
	low = 0
	high = len(ds_list)-1
	print "Binary Search"
	count = 1;
	while high >= low:
		#print(count)
		count += 1
		mid = (low+high)//2
		ds = ds_list[mid]
		midVal = InvertedIndexNode.getTerm(ds)
		if midVal < key:
			low = mid+1
		elif midVal > key:
			high = mid -1
		elif midVal == key:
			#Manipulating the candidate document list
			df = InvertedIndexNode.getDocFreq(ds)
			idf = InvertedIndexNode.getIdf(ds)
			tmp_node = InvertedIndexNode.getPostingListHead(ds)
			#print("Begin LinkedlIst")
			for j in range(df):
				#print("ASV")
				tmp_docId = PostingListNode.getDocId(tmp_node)
				#print(tmp_docId)
				candidate_document.add(tmp_docId)
				tmp_node = PostingListNode.getNextPostingList(tmp_node)
			#returning position
			return mid
	return -1

def constructQueryVector(qlist,query_tf_map,currCache):
	#print("0 term")
	#print(currCache.Dictionary_DS[0].term)
	magnitude = 0.0
	candidate_document = set()
	position_map = dict()
	query_vector = [0] * ss.readVocabSize()
	#print("inside cqv")
	for word in qlist:
		#print("word")
		#print(word)
		position_map[word] = binary_search(currCache.Dictionary_DS,word,candidate_document)
		#print("position")
		#print(position_map[word])
		query_term_df = float(query_tf_map[word])
		#print("query_tem_df")
		#print(query_term_df)
		query_term_position = position_map[word]
		if query_term_position >= 0 :
			query_vector[query_term_position] = query_term_df * currCache.idf_list[query_term_position]
			magnitude = magnitude + math.pow(query_vector[query_term_position],2)
			#print(magnitude)
	magnitude = round(math.sqrt(magnitude),3)
	#print(magnitude)
	return (magnitude,position_map,query_vector,candidate_document)

def calculateNQVector(qlist,query_magnitude,position_map,query_vector):
	norm_query_vector = [0] * ss.readVocabSize()
	for qp in range(len(query_vector)):
		if query_vector[qp] >= 0:
			norm_query_vector[qp] = round((query_vector[qp]/query_magnitude),3)
	return norm_query_vector

def calculateNormalisedQueryVector(qlist,query_magnitude,position_map,query_vector):
	norm_query_vector = [0] * ss.readVocabSize()
	for word in qlist:
		query_term_position = position_map[word]
		if query_term_position >= 0:
			norm_query_vector[query_term_position] = round((query_vector[query_term_position]/query_magnitude),3)
	return norm_query_vector


#term--> rows, document ---> columns
def calculateSimilarity(candidate_list,norm_query_vector,norm_matrix):
	similarity_map = dict()
	for doc in candidate_list:
		similarity = 0.0
		for j in range(vocab_size):
			if(norm_query_vector[j]> 0):
				similarity = similarity + (norm_matrix[j][doc-1]* norm_query_vector[j])
		similarity = round(similarity,3)
		similarity_map[doc] = similarity
	return similarity_map


def documentRanking(candidate_length,similarity_map):
	final_list = []
	similarity_map_sorted = dict()
	similarity_map_sorted = sorted(similarity_map.items(),key=lambda x:x[1])
	print "Document ID's in order"
	for i in reversed(range(candidate_length)):
		tuple = similarity_map_sorted[i]
		final_list.append(tuple[0])
	return final_list	
	
	
def select_query_terms(qlist,currCache,position_map):
	idf_map = dict()
	idf_map_sorted = dict()
	qlength = len(qlist)
	for word in qlist:
		location = position_map[word]
		idf_map[word] = currCache.idf_list[location]
	print(idf_map)	
	idf_map_sorted = sorted(idf_map.items(),key=lambda x:x[1])
	print("idf in order")
	print(idf_map_sorted)
	sel_qlist = []
	#Selects two terms
	new_final_list = []
	for i in reversed(range(qlength)):
		tuple = idf_map_sorted[i]
		sel_qlist.append(tuple[0])
	print("Selected qlist")
	print(sel_qlist)
	if(qlength > 1):
		new_final_list.append(sel_qlist[0])
		new_final_list.append(sel_qlist[1])
	print("new final list")
	print(new_final_list)
	return new_final_list
	
def find_term_candidate_document(word,currCache,position_map):
	Location = 	position_map[word]
	ds_list = currCache.Dictionary_DS
	ds = ds_list[Location]
	df = InvertedIndexNode.getDocFreq(ds)
	tmp_node = InvertedIndexNode.getPostingListHead(ds)
	candidate_position_map = dict()
	for j in range(df):
		tmp_docId = None
		tmp_positionList = None
		tmp_docId = PostingListNode.getDocId(tmp_node)
		tmp_positionList = PostingListNode.getDocTermPosition(tmp_node)
		candidate_position_map[tmp_docId] = tmp_positionList
		tmp_node = PostingListNode.getNextPostingList(tmp_node)
	return candidate_position_map
	
def find_min_distance(term1_candidate_document,term2_candidate_document,intersec_list):
	difference = dict()
	a = []
	b = []
	for docId in intersec_list:
		a = term1_candidate_document[docId]
		b = term2_candidate_document[docId]
		diff = 25
		for a1 in a:
			for b1 in b:
				if abs(int(a1)-int(b1)) < diff:
					diff = abs(int(a1)-int(b1))
		difference[docId] = diff
		a = []
		b = []
	#print(difference)
	return difference

def find_max_weight(diff_map):
	weigh_map = dict()
	for key,value in diff_map.items():
		val = (26 - int(value))
		percentage = float(val)/float(25)
		overall_per = round((0.3 * percentage),3)
		weigh_map[key] = overall_per
	return weigh_map
	
	
def	find_modified_similarity(similarity_map):
	mod_sim_map = dict()
	for key,value in similarity_map.items():
		val = round((0.7 * value),3)
		mod_sim_map[key]=val 
	return mod_sim_map


def calculate_total_sim_map(modified_sim_map,weightage_map):
	tot_sim_map = dict()
	for key,value in modified_sim_map.items():
		if key in weightage_map.keys():
			result = round((value + weightage_map[key]),3)
		else:
			result = round((value + 0.0),3)
		tot_sim_map[key]= result
	return tot_sim_map
	
def performSearch(query_tf_map,currCache,query_string):
	qlist = list()
	strippedQry = ""
	for key in query_tf_map:
		qlist.append(key);
	qlist.sort()
	print("Inside Search")
	print(qlist)
	for key in qlist:
		strippedQry+=key
	#Check if sorted qlist is present in out cache
	if strippedQry in query_cache.keys():
		final_list = query_cache[strippedQry].search_result
		similarity_map = query_cache[strippedQry].similarity_map
		return (final_list,similarity_map)
	else:
		output = constructQueryVector(qlist,query_tf_map,currCache)
		query_magnitude = output[0]
		position_map = output[1]
		#print("printing position map")
		#print(position_map)
		query_vector = output[2]
		candidate_document = output[3]
		if(len(qlist)>1):
			diff_map = dict()
			weightage_map = dict()
			term1_candidate_document = dict()
			term2_candidate_document = dict()
			term1_candidate_doc_list = []
			term2_candidate_doc_list = []
			select_qlist = select_query_terms(qlist,currCache,position_map)
			term1_candidate_document = find_term_candidate_document(select_qlist[0],currCache,position_map)
			term1_candidate_doc_list = term1_candidate_document.keys()
			term2_candidate_document = find_term_candidate_document(select_qlist[1],currCache,position_map)
			term2_candidate_doc_list = term2_candidate_document.keys()
			intersec_list = list(set(term1_candidate_doc_list).intersection(set(term2_candidate_doc_list)))
			if(len(intersec_list)>0):
				diff_map = find_min_distance(term1_candidate_document,term2_candidate_document,intersec_list)
			weightage_map = find_max_weight(diff_map)
			print("Printing the overall weightage")
			print(weightage_map)		
		norm_query_vector = calculateNormalisedQueryVector(qlist,query_magnitude,position_map,query_vector)
		candidate_list = list(candidate_document)
		candidate_list.sort()
		similarity_map=calculateSimilarity(candidate_list,norm_query_vector,currCache.norm_matrix)
		if(len(qlist)>1):
			modified_sim_map = dict()
			modified_sim_map = find_modified_similarity(similarity_map)
			total_sim_map = calculate_total_sim_map(modified_sim_map,weightage_map)
			print("Printing the total similarity")
			print(total_sim_map)
			final_list = documentRanking(len(candidate_document),total_sim_map)
			queryDetail = QueryDetail(query_vector,total_sim_map,final_list,qlist,position_map)
			relfeed_cache[query_string] = queryDetail
			query_cache[strippedQry] = queryDetail
			return (final_list,total_sim_map)
		else:
			final_list = documentRanking(len(candidate_document),similarity_map)
			queryDetail = QueryDetail(query_vector,similarity_map,final_list,qlist,position_map)
			#caching for future use
			print("Query String for search")
			#print(query_string)
			relfeed_cache[query_string] = queryDetail
			#print(relfeed_cache[query_string])
			query_cache[strippedQry] = queryDetail
			return (final_list,similarity_map)
	
	