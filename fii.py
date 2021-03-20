import requests
from bs4 import BeautifulSoup
import json
from unicodedata import normalize
import re
from models import Acao


def normalizar_string(texto):
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')


def remover_caracter_special(texto):
    return re.sub('[/!@#$().\n]', '', texto)


def get_fiis():
    dicionario = {}
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
    url = 'https://www.fundsexplorer.com.br/ranking'
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    table_tag = soup.find('table', attrs={'class' : 'table table-hover'})
    heads = table_tag.thead.find_all('th')
    cabecalho = []
    for head in heads:
        cabecalho.append(remover_caracter_special(normalizar_string(head.text.replace(' ', '_'))))
    
    rows = table_tag.tbody.find_all('tr')
    for row in rows:
        textos = [line for line in row.text.split('\n') if line != '']
        item = {}
        if textos[0] in dicionario:
            item = dicionario[textos[0]]
        for i in range(0, len(textos) -1):
            item[cabecalho[i]] = textos[i]
            dicionario[textos[0]] = item

    lista = list(dicionario.values())
    return json.dumps(lista, ensure_ascii=False, indent=3).encode('utf8')