import os
import redis
import re
from bs4 import BeautifulSoup

r = redis.Redis(host='localhost', port=6379, db=0)

def load_folder(path):
    files = os.listdir(path)
    print(files)
    for file in files:
        match = re.match(r'^book(\d+).html$', file)
        if match:
            with open(path + file) as f:
                html = f.read()
                book_id = match.group(1)              
                r.set(book_id, html)
                create_index(book_id, html)
            print(match.group(0), book_id)

def create_index(book_id, html):
    soup = BeautifulSoup(html, 'html.parser')
    texto = soup.get_text()
    lista_texto = texto.split(' ')
    for t in lista_texto:
        r.sadd(t, book_id)

load_folder('html/books/')
