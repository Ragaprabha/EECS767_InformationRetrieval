import InvertedIndexNode as iin
import PostingListNode as pln
import math

def readFromFiles():
    file_a_to_m = open('/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/InvertedIndex/InvertedIndexAtoM.txt','r')
    file_n_to_z = open('/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/InvertedIndex/InvertedIndexNtoZ.txt','r')
    list_a_to_m = populateInvertedIndex(file_a_to_m)
    list_n_to_z = populateInvertedIndex(file_n_to_z)
    list_a_to_m.extend(list_n_to_z)
    return list_a_to_m

def populateInvertedIndex(a_file):
    a_list = []
    lines = a_file.readlines()
    i = 0
    while i < len(lines):
        tmp = lines[i].split("\t")
        tempNode = iin.InvertedIndexNode(tmp[0], int(tmp[1]), int(tmp[2]), float(tmp[3]))
        is_first = True
        for j in range(tempNode.docFreq):
            i += 1
            tmpArray = lines[i].split("\t")
            if is_first:
            	docTermFrequency = int(tmpArray[1])
                docPositionList =[]
                for k in range(docTermFrequency):
					docPositionList.append(tmpArray[2+k].rstrip('\n'))
                head = pln.PostingListNode(int(tmpArray[0]),int(tmpArray[1]),docPositionList)
                tmp = head
                is_first = False
            else:
            	docTermFrequency = int(tmpArray[1])
                docPositionList =[]
                for k in range(docTermFrequency):
                    docPositionList.append(tmpArray[2+k].rstrip('\n'))
                tmp.next = pln.PostingListNode(int(tmpArray[0]),int(tmpArray[1]),docPositionList)
                tmp = tmp.next
        tempNode.postingListHead = head
        a_list.append(tempNode)
        i += 1
    return a_list

def create_inverted_index(vocab,vocab_df_list,vocab_tf_list,doc_list_map,position_list_map,doc_size):
    inverted_index = []
    vocab.sort()
    for term in vocab:
        df_set = vocab_df_list.get(term)
        df = len(df_set)
        idf = round(math.log10(float(float(doc_size)/float(df))),3)
        tf = vocab_tf_list.get(term)
        temp_entry = iin.InvertedIndexNode(term,df,tf,idf)
        is_first = True
        for i in df_set:
            doc_term_freq = doc_list_map[i - 1].get(term)
            doc_term_position = position_list_map[i-1].get(term)
            if is_first:
                head = pln.PostingListNode(i,doc_term_freq,doc_term_position)
                temp = head
                is_first = False
            else:
                temp.next = pln.PostingListNode(i,doc_term_freq,doc_term_position)
                temp = temp.next
        temp_entry.postingListHead = head
        inverted_index.append(temp_entry)
    return inverted_index

def create_posting_list_files(inverted_index):
    # File 1 contains posting lists for all terms a-m
    # File 2 contains posting lists for all terms n-z
    file_a_to_m = open('/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/InvertedIndex/InvertedIndexAtoM.txt','w+')
    file_n_to_z = open('/Users/Ragaprabha/djangoWebServer/IRProject/relfeedback/src/InvertedIndex/InvertedIndexNtoZ.txt','w+')
    index = 0
    for i in range(len(inverted_index)):
        if not inverted_index[i].term[0] < 'n':
            index = i
            break;
    list_a_to_m = inverted_index[:index]
    list_n_to_z = inverted_index[index:]
    for i in range(len(list_a_to_m)):
        tempNode = list_a_to_m[i]
        file_a_to_m.write(str(tempNode.term)+"\t"+str(tempNode.docFreq)+"\t"+str(tempNode.termFreq)+"\t"+str(tempNode.idf)+"\n")
        tempPost = tempNode.postingListHead
        while tempPost != None:
            file_a_to_m.write(str(tempPost.docId)+"\t"+str(tempPost.docTermFreq)+"\t"+str('\t'.join(format(tempPost.docTermPosition[x]) for x in range(tempPost.docTermFreq)))+"\n")
            tempPost = tempPost.next
    file_a_to_m.close()
    for i in range(len(list_n_to_z)):
        tempNode = list_n_to_z[i]
        file_n_to_z.write(str(tempNode.term)+"\t"+str(tempNode.docFreq)+"\t"+str(tempNode.termFreq)+"\t"+str(tempNode.idf)+"\n")

        tempPost = tempNode.postingListHead
        while tempPost != None:
            file_n_to_z.write(str(tempPost.docId)+"\t"+str(tempPost.docTermFreq)+"\t"+str('\t'.join(format(tempPost.docTermPosition[x]) for x in range(tempPost.docTermFreq)))+"\n")
            tempPost = tempPost.next
    file_n_to_z.close()