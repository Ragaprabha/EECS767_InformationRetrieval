class QueryDetail:
	query_vector = None
	similarity_map =  None
	search_result = None
	qlist = None
	positionMap = None

	def __init__(self,query_vector,similarity_map,search_result,qlist,positionMap):
		self.query_vector = query_vector
		self.similarity_map = similarity_map
		self.search_result = search_result
		self.qlist = qlist
		self.positionMap = positionMap
