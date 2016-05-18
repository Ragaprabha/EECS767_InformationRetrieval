import vectorSpaceModel
class Cache:
	original_matrix = None
	norm_matrix = None
	Dictionary_DS = None
	idf_list = None
	
	def __init__(self,original_matrix,norm_matrix,Dictionary_DS,idf_list):
		self.original_matrix = original_matrix
		self.norm_matrix = norm_matrix
		self.Dictionary_DS = Dictionary_DS
		self.idf_list = idf_list
	
	@staticmethod
	def getVSM(self):
		return self.norm_matrix

	@staticmethod
	def getInvIndex(self):
		return self.Dictionary_DS

	@staticmethod
	def getIdfList(self):
		return self.idf_list


