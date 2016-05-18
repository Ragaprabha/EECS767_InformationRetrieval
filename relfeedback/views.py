from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from src import	queryProcessing as qp
import time

# Create your views here.
@csrf_exempt
def index(request):
	if request.method == 'GET':
		return render(request, 'relfeedback/index.html', {})
	elif request.method == 'POST':
		do_rel_feedback = request.POST.get('relfeed')
		if do_rel_feedback != None:
			doc_list = request.POST.getlist('result')
			tempvar = request.POST['searchquery']
			res = relFeedProc(doc_list,tempvar)
			file_list = res[0]
			sim_list = res[1]
			output = list()
			for i in range(len(file_list)):
				output.append((file_list[i],sim_list[i]))
			difference = res[2]
		else:
			tempvar = request.POST['searchquery']
			res = queryProc(tempvar)
			
			file_list = res[0]
			sim_list = res[1]
			output = list()
			for i in range(len(file_list)):
				output.append((file_list[i],sim_list[i]))
			difference = res[2]
		return render(request, 'relfeedback/index.html', {'file_list' : output, 'sim_list' : sim_list, 'title':'abc','sq':tempvar,'diff':difference})
		
def queryProc(query):
	output = qp.processQuery(query.rstrip().lower())
	return output

def relFeedProc(doc_list,query):
	print "Relevance feedback"
	print (len(doc_list))
	print(doc_list)
	print("query")
	print(query)
	output = qp.processQueryRelFeed(doc_list,query.rstrip().lower())
	return output

def originalFiles(request):
	print "##################1"
	print request.path
	template = loader.get_template(request.path)
	return HttpResponse(template.render())