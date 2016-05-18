from urlparse import urlparse
import os
import sys

#This function returns the domain name of the given URL
def get_domain(url):
    try:
        results = urlparse(url).netloc.split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)

def create_project_dir_data(directory):
    if not os.path.exists(directory):
        print('Creating data directory ' + directory)
        os.makedirs(directory)
#create_data_files(html_bytes,urlname,Spider.data_file)

def create_data_stores(data,file_name,path):
    file_path =path+'/'+file_name+'.htm'
    if not os.path.isfile(file_path):
        write_file(file_path,data)


def create_data_files(urlfrontier, urlcrawled, base_url):
    urlfrontier_holder = urlfrontier
    urlcrawled_holder = urlcrawled
    if not os.path.isfile(urlfrontier_holder):
        write_file(urlfrontier_holder, base_url)
    if not os.path.isfile(urlcrawled_holder):
        write_file(urlcrawled_holder, '')



def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
        return results


def write_file(path, data):
    try:
        f = open(path, 'w')
        f.write(data)
        f.close()
    except:
        print('Exception occured in writing the file', sys.exc_info()[0])


def delete_file_contents(path):
    with open(path, 'w'):
        pass


def set_to_file(links_queue, file):
    delete_file_contents(file)
    sorted_links = sorted(links_queue)
    for link in sorted_links:
        append_to_file(file, link)


def append_to_file(path, data):
    with open(path, mode='a') as file:
        file.write((data + '\n').encode("utf8"))

