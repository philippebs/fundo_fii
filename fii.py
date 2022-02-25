import requests
from bs4 import BeautifulSoup
import json
from unicodedata import normalize
import re
from models import FiiOld, Fii, Investimento, save_one_models, save_all_models
from datetime import date, datetime
from enums.tipo import TipoInvestimento
from sqlalchemy import inspect
from flask import jsonify

def normalizar_string(texto):
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')


def remover_caracter_special(texto):
    return re.sub('[/!@#$().\n]', '', texto)


def convert_to_json(fiis):
    fiisArr = []
    for fii in fiis:
        fiisArr.append(fii.to_dict(show=['investimento', 'investimento.codigo'])) 
    return fiisArr


def convert_to_json_investimento(investimentos):
    investimentosArr = []
    for investimento in investimentos:
        investimentosArr.append(investimento.to_dict()) 
    return investimentosArr


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

        fii = FiiOld(link, codigo_fundo, setor, preco_atual, liquidez_diaria, dividendo, dividend_yield, dy_3m_acumulado, dy_6m_acumulado, dy_12m_acumulado,
                dy_3m_media, dy_6m_media, dy_12m_media, dy_ano, variacao_preco, rentabilidade_periodo, rentabilidade_acumulada, patrimonio_liq,
                vpa, pvpa, dy_patrimonial, variacao_patrimonial, rentabilidade_patrno_periodo, rentabilidade_patr_acumulada, vacancia_fisica,
                vacancia_financeira, quantidade_ativos)
        lista_fundos.append(fii)

    return json.dumps(lista_fundos, ensure_ascii=False, default=lambda o: o.__dict__, indent=3)


def create_fiis():
    lista_fundos = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
    url_base = 'https://www.fundsexplorer.com.br'
    url = url_base + '/ranking'
    response = requests.get(url, headers=headers, timeout=10)
    
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    table_tag = soup.find('table', attrs={'class' : 'table table-hover'})
    rows = table_tag.tbody.find_all('tr')
    list_investimentos = []
    investimentos = Investimento.query.filter(Investimento.ativo == True, Investimento.tipo == TipoInvestimento.FII.value).all()
    for row in rows:
        column = [line for line in row.text.split('\n')]
        codigo_fundo = column[1]
        setor = column[2]
        investimento = Investimento(codigo=codigo_fundo, tipo=TipoInvestimento.FII.value, descricao=setor)
        if investimento  not in investimentos:
            list_investimentos.append(investimento)
            # save_one_models(investimento)
            print(investimento)
    save_all_models(list_investimentos)


def get_fiis_codes():
    investimentos = Investimento.query.filter(Investimento.ativo == True, Investimento.tipo == TipoInvestimento.FII.value).all()
    if len(investimentos) == 0:
        create_fiis()
    return convert_to_json_investimento(investimentos)


def get_fiis_v1():
    date_today = date.today()
    fiis = Fii.query.filter(Fii.data_importacao == date_today).all()
    if len(fiis) > 0:
        print("Retorno do banco")
        return convert_to_json(fiis)

    investimentos = Investimento.query.filter(Investimento.ativo == True, Investimento.tipo == TipoInvestimento.FII.value).all()
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
        investimento = Investimento(codigo=codigo_fundo, tipo=TipoInvestimento.FII.value, descricao=setor)
        index_investimento = -1
        try:
            index_investimento = investimentos.index(investimento)
        except:
            index_investimento = -1

        if index_investimento > -1:
            investimento = investimentos[index_investimento]
        else:
            save_one_models(investimento)

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

        fii = Fii(investimento.id, date_today, setor, preco_atual, liquidez_diaria
                , dividendo, dividend_yield, dy_3m_acumulado, dy_6m_acumulado, dy_12m_acumulado,
                dy_3m_media, dy_6m_media, dy_12m_media, dy_ano, variacao_preco, rentabilidade_periodo, rentabilidade_acumulada, patrimonio_liq,
                vpa, pvpa, dy_patrimonial, variacao_patrimonial, rentabilidade_patrno_periodo, rentabilidade_patr_acumulada, vacancia_fisica,
                vacancia_financeira, quantidade_ativos)
        # save_one_models(fii)
        lista_fundos.append(fii)
    save_all_models(lista_fundos)
    # return json.dumps(lista_fundos, ensure_ascii=False, default=lambda o: o.__dict__, indent=3)
    return convert_to_json(lista_fundos)


if __name__ == "__main__":
    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    print(date.today())
    # fii = Fii(1, "Teste", "rdrd", "dfdf")
    # save_models(fii)
    # create_fiis()
    # investimentos = Investimento.query.filter(Investimento.ativo == True, Investimento.tipo == TipoInvestimento.FII.value).all()
    
    # investimento = Investimento(codigo="FIVN11", tipo=TipoInvestimento.FII.value, descricao="Shoppings")
    # fiis = Fii.query.all()
    
    # print("Método antigo")
    # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    # json_antigo = get_fiis()
    # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    # print("Método novo salvando no banco")
    # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    # json_novo = get_fiis_v1()
    print(get_fiis_v1())
    # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    # # date_today = datetime.today().strftime('%Y-%m-%d')
    # # fii = Fii.query.filter(Fii.data_importacao == date_today).all()
    # # if len(fii) > 0:
    # #     print("teste")
    # # print()
    # if investimento  not in investimentos:
    #     print("True")
    # else:
    #     print("False")
    # print(len(investimentos))
    # print(TipoInvestimento.FII)
    # print(str(TipoInvestimento.FII))
    # print(TipoInvestimento.FII.value)
    # print(TipoInvestimento.FII.name)
    # print()
    # investimento = Investimento(codigo="FII_1", tipo=TipoInvestimento.FII.value)
    # save_models(investimento)
    # # get_fiis()
    # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    # print(get_fii_model())
    # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))