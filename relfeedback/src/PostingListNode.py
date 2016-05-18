class PostingListNode:
    docId = None
    docTermFreq = None
    docTermPosition = None
    next = None

    def __init__(self, a_docid, a_doc_term_freq,a_doc_term_position):
        self.docId = a_docid
        self.docTermFreq = a_doc_term_freq
        self.docTermPosition = a_doc_term_position

    def next_posting_list(self, a_posting_list_node):
        self.next = a_posting_list_node


    def getDocId(self):
        return self.docId

    def getDocTermFreq(self):
        return self.docTermFreq
        
    def getDocTermPosition(self):
        return self.docTermPosition

    def getNextPostingList(self):
        return self.next