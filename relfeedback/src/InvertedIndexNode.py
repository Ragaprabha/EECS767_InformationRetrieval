class InvertedIndexNode:
    term = None
    docFreq = None
    termFreq = None
    postingListHead = None
    idf = None

    def __init__(self,a_term,a_doc_freq,a_term_freq,idf):
        self.term = a_term
        self.docFreq = a_doc_freq
        self.termFreq = a_term_freq
        self.idf = idf

    def add_posting_list(self,a_posting_list):
        self.postingListHead = a_posting_list

    @staticmethod
    def getTerm(self):
        return self.term

    @staticmethod
    def getDocFreq(self):
        return self.docFreq

    @staticmethod
    def getTermFreq(self):
        return self.termFreq

    @staticmethod
    def getPostingListHead(self):
        return self.postingListHead
    @staticmethod
    def getIdf(self):
        return self.idf