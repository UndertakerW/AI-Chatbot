# Before using this .py
# Install googlesearch by
# 1. cd ChatBot\packages\googlesearch
# 2. python setup.py install

from googlesearch import search
from urllib import request
from bs4 import BeautifulSoup

import asyncio
from time import sleep

def searchKeyword(keyword, num_results=10):
    result = list()
    for url in search(keyword, stop=num_results, pause=0):
        #print(url)
        try:
            html = request.urlopen(url).read().decode('utf8')
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            result.append((title.string, url))
        except:
            result.append(('Webpage', url))
    return result

def botSearchKeyword(ui, keyword, num_results=10):
    result = searchKeyword(keyword, num_results=10)
    text = ''
    for (title, url) in result:
        text += title
        text += '\n'
        text += url
        text += '\n'
    #ui.bot_output.emit(text)
    #print('search done')
    return text
    

    