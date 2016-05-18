import urllib
import sys
from urlparse import urljoin
from bs4 import BeautifulSoup
from Helper import *
import re

class Spider:

    # Class variables
    project_name = ''
    data_file = ''
    base_url = ''
    domain_name = ''
    urlfrontier_file = ''
    urlcrawled_file = ''
    urlfrontier = set()
    crawled = set()

    def __init__(self, project_name,data_file, base_url, domain_name,urlfrontier_path,urlcrawled_path):
        Spider.project_name = project_name
        Spider.data_file = data_file
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.urlfrontier_file = urlfrontier_path
        Spider.urlcrawled_file = urlcrawled_path
        self.initialSetup()
        self.crawl_page('Main Spider', Spider.base_url)



    #Initial Setup done by main spider for the first time
    @staticmethod
    def initialSetup():
        create_project_dir(Spider.project_name)
        #create_project_dir_data(Spider.data_file)
        create_data_files(Spider.urlfrontier_file,Spider.urlcrawled_file, Spider.base_url)
        Spider.urlfrontier = file_to_set(Spider.urlfrontier_file)
        Spider.crawled = file_to_set(Spider.urlcrawled_file)


    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' crawling: ' + page_url)
            print('Number of URLs in URLFrontier ' + str(len(Spider.urlfrontier)) + ' | Number of URLs Crawled ' + str(len(Spider.crawled)))
            output = Spider.collect_links(page_url)
            urlcollection = output[0]
            urlname = output[1]
            html_bytes = output[2]
            Spider.add_links_to_queue(urlcollection)
            Spider.urlfrontier.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()
            #create_data_stores(html_bytes,urlname,Spider.data_file)



    @staticmethod
    def collect_links(page_url):
        html_string = ''
        try:
            response = urllib.urlopen(page_url)
            if response.info().type == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            output = Spider.FindLinks(Spider.base_url, page_url,html_string)
            urlcollection = output[0]
            urlname = output[1]
        except:
            print('Exception occured:cannot crawl webpage', sys.exc_info()[0])
            return set()
        return (urlcollection,urlname,html_bytes)

    @staticmethod
    def FindLinks(base_url,page_url,html_string):
        page_links = set()
        soup = BeautifulSoup(html_string,"html.parser")
        name = soup.title.string
        #print("Printing")
        #print(name)
        pattern = re.compile("\\s")
        name = re.sub(re.compile('\\|'),'',name)
        name = re.sub(re.compile('\\-'),'',name)
        name = re.sub(re.compile('\\/'),'',name)
        name = re.sub(pattern,'_',name)
        for tag in soup.findAll('a',href=True):
            new_url = urljoin(base_url,tag['href'])
            page_links.add(new_url)
        return (page_links,name)



    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            #print url
            if url in Spider.urlfrontier:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.urlfrontier.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.urlfrontier, Spider.urlfrontier_file)
        set_to_file(Spider.crawled, Spider.urlcrawled_file)
