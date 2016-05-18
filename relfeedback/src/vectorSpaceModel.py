
import stopliststemmer
import invertedIndex as ii
from InvertedIndexNode import InvertedIndexNode
from PostingListNode import PostingListNode
import math

# Reading the dictionary, posting list datastructure, document and vocabulary size
Dict_DS = ii.readFromFiles()
doc_size = stopliststemmer.readDocSize()
vocab_size = stopliststemmer.readVocabSize()
vocab_size = stopliststemmer.readVocabSize()
matrix = []


print("vocab_size")
print(vocab_size)
print("doc_size")
print(doc_size)
print("dict")
print("End")
idf_list = [0] * vocab_size
magnitude = [0] * doc_size
df = 0
def populateMatrix():
    i = 0
    for ds in Dict_DS:
        #print(" one ")
        df = InvertedIndexNode.getDocFreq(ds)
        idf_list[i] = round(math.log10(float(float(doc_size)/float(df))),3)
        temp_tfidf_list = [0]* doc_size
        tmp_node = InvertedIndexNode.getPostingListHead(ds)
        for j in range(df):
            tmp_docId = PostingListNode.getDocId(tmp_node)
            temp_tfidf_list[tmp_docId - 1] = tmp_node.docTermFreq * idf_list[i]
            tmp_node = PostingListNode.getNextPostingList(tmp_node)
        matrix.append(temp_tfidf_list)
        i = i+1
    return matrix

matrix = populateMatrix()
# print matrix
norm_matrix = list(matrix)
# print "duplication"
# print norm_matrix

def calculateMagnitude():
    for i in range(doc_size):
        for j in range(vocab_size):
            #print("two")
            magnitude[i] =   magnitude[i] + math.pow(matrix[j][i],2)
            #print(magnitude[i])
        magnitude[i] = round(math.sqrt(magnitude[i]),3)
    return magnitude

magnitude = calculateMagnitude()

#print magnitude

def normalizeMatrix():
    # matrix = populateMatrix()
    # magnitude = calculateMagnitude()
    # norm_matrix = list(matrix)
    for i in range(doc_size):
        for j in range(vocab_size):
            if magnitude[i] == 0.0:
			    norm_matrix[j][i] = 0.0
            else:
                norm_matrix[j][i] =  round(matrix[j][i]/magnitude[i],3)
    return norm_matrix

matrix_new = normalizeMatrix()
#print matrix_new

def saveDocumentMagniture(magnitude):
	f = open('/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/etc/DocMagnitude.txt','w+')
	for i in range(len(magnitude)):
		f.write(str(i)+"\t"+str(magnitude[i])+"\n")
	f.close
	
""""def readDocumentLength():
	docMagMap = dict()
	f = open('C:/Users/Bijal/workspace/django/websearch/relfeedback/etc/DocMagnitude.txt','r+')
	for line in f.readlines()
	tmp = line.split("\t")
	docMap[int(tmp[0].rstrip())] = float(tmp[1].rstrip())"""
		
	