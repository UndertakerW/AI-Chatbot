# Before using this .py
# Install googlesearch by
# 1. cd ChatBot\packages\googlesearch
# 2. python setup.py install

from googlesearch import search

def searchKeyword(keyword):
    for url in search(keyword, stop=20):
        print(url)
        