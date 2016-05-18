import re

def cleanhtml(raw_html):
  f = open(raw_html,'r')
  cleanr =re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', f.read())
  return cleantext

from bs4 import BeautifulSoup

def parseFile(file_name):
    f = open(file_name,'r')
    soup = BeautifulSoup(f)
    t = soup.getText()
    print(t)

def remove_pattern(pattern,file_data):
    pattern_format = re.compile(pattern)
    file_data = re.sub(pattern_format,'',file_data)
    return file_data

def remove_script_tag_between(file_data):
    i = 0;
    while(file_data.find("script") != -1):
        i += 1
        print(i)
        begin_pos = file_data.index("\<script")
        end_pos = file_data.index("\<\\script\>")
        if(end_pos > 0):
            file_data = file_data[:begin_pos] + file_data[begin_pos+end_pos+10:]
    return file_data

def parse_html(file_name):
    f = open(file_name,'r')
    file_data = f.read()
    #print(type(file_data))
    file_data = remove_pattern('\\<[^>]*>',file_data)
    file_data = remove_pattern('&#160;',file_data)
    file_data = remove_pattern('(?s)<!.*?(/>|<-->)',file_data)
    file_data = remove_pattern('\\<[^>]*>',file_data)
    file_data = remove_pattern('(?m)^[ \t]*\r?\n',file_data)
    file_data = remove_pattern('/(<script[^>]*>.+?<\/script>|<style[^>]*>.+?<\/style>)/s',file_data)
    #file_data = remove_script_tag_between(file_data)
    return file_data

#print(parse_html("Original Files/Acadia_National_Park.htm"))

# code for fetching file from directories
import os




