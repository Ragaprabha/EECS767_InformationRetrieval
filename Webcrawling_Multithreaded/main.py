import threading
import sys
from Queue import Queue
from spider import Spider
from urlparse import urlparse
from Helper import *
import time


PROJECT_NAME = 'wikiCrawler'
HOMEPAGE = 'https://en.wikipedia.org/'
DATA_FILE = 'DataStore'
DOMAIN_NAME = get_domain(HOMEPAGE)
#print("Domain name"+" " +DOMAIN_NAME)
URLFRONTIER_FILE = PROJECT_NAME + '/urlfrontier.txt'
URLCRAWLED_FILE = PROJECT_NAME + '/urlcrawled.txt'
NUMBER_OF_THREADS = 2
NUMBER_OF_PAGES_TO_CRAWL = 1000
queue = Queue()
start_time = time.time()
Spider(PROJECT_NAME,DATA_FILE, HOMEPAGE, DOMAIN_NAME,URLFRONTIER_FILE,URLCRAWLED_FILE)


# Create sub threads
def create_subthreads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    i=0
    while i<= NUMBER_OF_PAGES_TO_CRAWL :
    #while True:
        try:
            #print("ivalue" +" "+str(i))
            url = queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            queue.task_done()
            i = i+1
        except:
            print('Exception occured:', sys.exc_info()[0])
            continue
    print("--- %s seconds ---" % (time.time() - start_time))

    #sys.exit(0)

# Each queued link is a new job
def queue_jobs():
    for link in file_to_set(PROJECT_NAME + '/urlfrontier.txt'):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(PROJECT_NAME + '/urlfrontier.txt')
    if len(queued_links) > 0:
        #print(str(len(queued_links)) + ' links in the queue')
        queue_jobs()

create_subthreads()
crawl()