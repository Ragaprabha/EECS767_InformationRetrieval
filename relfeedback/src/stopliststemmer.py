"""
Author: Bijal Parikh
File Description : Code to remove stop words from HTML parsed files, stem them and add to output file
project : EECS 767 Information Retrieval
"""
import snowballstemmer as sst
import os
import invertedIndex as ii
import re
from django.utils.encoding import *
from collections import defaultdict

def getStopWords():
	stopFile = open('/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/StopFile.txt','r')
	stopWords = set()
	for line in stopFile:
		for word in line.split(" "):
			stopWords.add(word.rstrip())
	stopFile.close()
	return stopWords

def get_all_files():
	list_of_files = list()
	for file in os.listdir("/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/parsedFiles/"):
		list_of_files.append(file)
	return list_of_files



def readVocabSize():
	return 16612


def readDocSize():
	return 392

def createIndex():
	stemmer = sst.PorterStemmer()
	vocab = set()
	vocab_list = []
	docListMap = []
	positionListMap = []
	vocabDFList = dict()
	vocabTFList = dict()
	#instead of fetching filenames from flat file, fetch file name from dir itself using os.listdir
	docId = 0
	matchWords = re.compile("^[a-z|A-Z]+$")
	list_of_files = get_all_files()
	stopWords = getStopWords()
	print("Size of list")
	print(len(list_of_files))
	for file in list_of_files:
		docId += 1
		positionCount = 0
		#tempFileName = line.rstrip()
		#print(tempFileName)
		tempInFile = open('/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/parsedFiles/'+file,'r')
		outFileName = 'noStop'+file
		tempOutFile = open('/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/noStop/'+outFileName,'w+')
		tempMap = dict()
		positionMap = defaultdict(list)
		positionTuple = []
		for tempLine in tempInFile.readlines():
			for tempWord in tempLine.split():
				tempWord = tempWord.rstrip().lower()
				if tempWord not in stopWords:
					# Stem the word before writing it in outFile
					try:
						stemmedWord =stemmer.stemWord(tempWord)
						if matchWords.match(stemmedWord):
							vocab.add(stemmedWord)
							#print(stemmedWord)
							#print("StemmedWord " + stemmedWord)
							# Take care of term frequency
							if tempMap.has_key(stemmedWord):
								count = tempMap.get(stemmedWord) + 1
							else:
								count = 1
							tempMap[stemmedWord] = count
							#Take care of position
							positionCount = positionCount+1
							positionTuple.append((stemmedWord,positionCount))
							#Take care of document frequency
							if vocabDFList.has_key(stemmedWord):
								docIdSet = vocabDFList.get(stemmedWord)
							else:
								docIdSet = set()
							docIdSet.add(docId)
							vocabDFList[stemmedWord] = docIdSet
							#Take care of overall term frequency
							if vocabTFList.has_key(stemmedWord):
								totalCount = vocabTFList.get(stemmedWord)  + 1
							else:
								totalCount = 1
							vocabTFList[stemmedWord] = totalCount
							#Finally write it in OutFile
							tempOutFile.write(stemmedWord)
							tempOutFile.write(" ")
					except UnicodeDecodeError:
						#Create a vocabulary
						print('stemming')
		docListMap.append(tempMap)
		for k,v in positionTuple:
			positionMap[k].append(v)
		positionListMap.append(positionMap)
	docSize = docId
	vocabSize = len(vocab)
	print("Printing DocSize")
	print(docSize)
	print("Printing New Vocabulary Size")
	print(vocabSize)
	tempOutFile.close()
	tempInFile.close()
	vocab_list = list(vocab)
	print("vocab list len")
	print(len(vocab_list))
	inverted_index = ii.create_inverted_index(vocab_list,vocabDFList,vocabTFList,docListMap,positionListMap,docSize)
	ii.create_posting_list_files(inverted_index)
	
createIndex()



