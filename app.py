from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import acao

import requests
from bs4 import BeautifulSoup
import json
from unicodedata import normalize
import re
from models import Fii


#Inicializa nossa aplicacao Flask
app =  Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#Cria a rota para o caminho
@app.route("/")
@cross_origin()
def index():
	return render_template('index.html')


@app.route("/api/resources/fii")
@cross_origin()
def fundo_fii():
	lista_fundos = []
	headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
	url_base = 'https://www.fundsexplorer.com.br'
	url = url_base + '/ranking'
	response = requests.get(url, headers=headers, timeout=10)
	
	soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
	table_tag = soup.find('table', attrs={'class' : 'table table-hover'})
	rows = table_tag.tbody.find_all('tr')

	for row in rows:
		link = url_base + row.select('td:nth-child(1) > a')[0].get('href')
		codigo_fundo = row.select('td:nth-child(1) > a')[0].text
		setor = row.select('td:nth-child(2)')[0].text
		preco_atual = row.select('td:nth-child(3)')[0].text
		liquidez_diaria = row.select('td:nth-child(4)')[0].text
		dividendo = row.select('td:nth-child(5)')[0].text
		dividend_yield = row.select('td:nth-child(6)')[0].text
		dy_3m_acumulado = row.select('td:nth-child(7)')[0].text
		dy_6m_acumulado = row.select('td:nth-child(8)')[0].text
		dy_12m_acumulado = row.select('td:nth-child(9)')[0].text
		dy_3m_media = row.select('td:nth-child(10)')[0].text
		dy_6m_media = row.select('td:nth-child(11)')[0].text
		dy_12m_media = row.select('td:nth-child(12)')[0].text
		dy_ano = row.select('td:nth-child(13)')[0].text
		variacao_preco = row.select('td:nth-child(14)')[0].text
		rentabilidade_periodo = row.select('td:nth-child(15)')[0].text
		rentabilidade_acumulada = row.select('td:nth-child(16)')[0].text
		patrimonio_liq = row.select('td:nth-child(17)')[0].text
		vpa = row.select('td:nth-child(18)')[0].text
		pvpa = row.select('td:nth-child(19)')[0].text
		dy_patrimonial = row.select('td:nth-child(20)')[0].text
		variacao_patrimonial = row.select('td:nth-child(21)')[0].text
		rentabilidade_patrno_periodo = row.select('td:nth-child(22)')[0].text
		rentabilidade_patr_acumulada = row.select('td:nth-child(23)')[0].text
		vacancia_fisica = row.select('td:nth-child(24)')[0].text
		vacancia_financeira = row.select('td:nth-child(25)')[0].text
		quantidade_ativos = row.select('td:nth-child(26)')[0].text

		fii = Fii(link, codigo_fundo, setor, preco_atual, liquidez_diaria, dividendo, dividend_yield, dy_3m_acumulado, dy_6m_acumulado, dy_12m_acumulado,
		dy_3m_media, dy_6m_media, dy_12m_media, dy_ano, variacao_preco, rentabilidade_periodo, rentabilidade_acumulada, patrimonio_liq,
		vpa, pvpa, dy_patrimonial, variacao_patrimonial, rentabilidade_patrno_periodo, rentabilidade_patr_acumulada, vacancia_fisica,
		vacancia_financeira, quantidade_ativos)
		lista_fundos.append(fii)

	return json.dumps(lista_fundos, ensure_ascii=False, default=lambda o: o.__dict__, indent=3)


@app.route('/api/resources/acao/<nome_acao>')
@cross_origin()
def fund_acao(nome_acao):
	return acao.get_cotacao(nome_acao)
	

#Executa nossa aplicacao
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

