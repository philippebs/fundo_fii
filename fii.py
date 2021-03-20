import requests
from bs4 import BeautifulSoup
import json
from unicodedata import normalize
import re
from models import Fii
from datetime import datetime

def normalizar_string(texto):
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')


def remover_caracter_special(texto):
    return re.sub('[/!@#$().\n]', '', texto)


def get_fiis():
    lista_fundos = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
    url_base = 'https://www.fundsexplorer.com.br'
    url = url_base + '/ranking'
    response = requests.get(url, headers=headers, timeout=10)
    
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    table_tag = soup.find('table', attrs={'class' : 'table table-hover'})
    rows = table_tag.tbody.find_all('tr')

    for row in rows:
        column = [line for line in row.text.split('\n')]
        codigo_fundo = column[1]
        link = url_base + '/funds/' + codigo_fundo.lower()
        setor = column[2]
        preco_atual = column[3]
        liquidez_diaria = column[4]
        dividendo = column[5]
        dividend_yield = column[6]
        dy_3m_acumulado = column[7]
        dy_6m_acumulado = column[8]
        dy_12m_acumulado = column[9]
        dy_3m_media = column[10]
        dy_6m_media = column[11]
        dy_12m_media = column[12]
        dy_ano = column[13]
        variacao_preco = column[14]
        rentabilidade_periodo = column[15]
        rentabilidade_acumulada = column[16]
        patrimonio_liq = column[17]
        vpa = column[18]
        pvpa = column[19]
        dy_patrimonial = column[20]
        variacao_patrimonial = column[21]
        rentabilidade_patrno_periodo = column[22]
        rentabilidade_patr_acumulada = column[23]
        vacancia_fisica = column[24]
        vacancia_financeira = column[25]
        quantidade_ativos = column[26]

        fii = Fii(link, codigo_fundo, setor, preco_atual, liquidez_diaria, dividendo, dividend_yield, dy_3m_acumulado, dy_6m_acumulado, dy_12m_acumulado,
                dy_3m_media, dy_6m_media, dy_12m_media, dy_ano, variacao_preco, rentabilidade_periodo, rentabilidade_acumulada, patrimonio_liq,
                vpa, pvpa, dy_patrimonial, variacao_patrimonial, rentabilidade_patrno_periodo, rentabilidade_patr_acumulada, vacancia_fisica,
                vacancia_financeira, quantidade_ativos)
        lista_fundos.append(fii)

    return json.dumps(lista_fundos, ensure_ascii=False, default=lambda o: o.__dict__, indent=3)

if __name__ == "__main__":
    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    # # get_fiis()
    # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    # print(get_fii_model())
    # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))