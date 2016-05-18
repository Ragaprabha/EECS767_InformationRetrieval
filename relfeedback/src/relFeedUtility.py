import math
import snowballstemmer
import vectorSpaceModel
import stopliststemmer
import invertedIndex as ii
from InvertedIndexNode import InvertedIndexNode
from PostingListNode import PostingListNode
from cache import *
from searchUtility import *

def performRelFeedback(qlist,query_tf_map,currCache):
	qlist = list()
	for key in query_tf_map:
		qlist.append(key)
	qlist.sort()
	SearchUtility.constructQueryVector(qlist,query_tf_map,currCache)
	
def performSearch(query_tf_map,currCache):
	qlist = list()
	for key in query_tf_map:
		qlist.append(key);
	qlist.sort()
	output = constructQueryVector(qlist,query_tf_map,currCache)
	query_magnitude = output[0]
	position_map = output[1]
	query_vector = output[2]
	candidate_document = output[3]
	norm_query_vector = calculateNormalisedQueryVector(qlist,query_magnitude,position_map,query_vector)
	candidate_list = list(candidate_document)
	print("CandidATE")
	for term in candidate_list:
		print(term)
	candidate_list.sort()
	similarity_map=calculateSimilarity(candidate_list,norm_query_vector,currCache.norm_matrix)
	final_list = documentRanking(len(candidate_document),similarity_map)
	print("Terms are here")
	for term in final_list:
		print(term)
	return final_list
	