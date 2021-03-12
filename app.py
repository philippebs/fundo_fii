from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
import statusInvest

#Inicializa nossa aplicacao Flask
app =  Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Cria a rota para o caminho
@app.route("/")
@cross_origin()
def index():
	return render_template('index.html')

@cross_origin()
@app.route("	")
def fundo_fii():
	dicionario = {}
	headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
	url = 'https://www.fundsexplorer.com.br/ranking'
	response = requests.get(url, headers=headers, timeout=10)
	soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
	table_tag = soup.find('table', attrs={'class' : 'table table-hover'})
	heads = table_tag.thead.find_all('th')
	cabecalho = []
	for head in heads:
		cabecalho.append(head.text)
		
	rows = table_tag.tbody.find_all('tr')
	for row in rows:
		textos = [line for line in row.text.split('\n') if line != '']
		item = {}
		if textos[0] in dicionario:
			item = dicionario[textos[0]]
		for i in range(0, len(textos) -1):
			item[cabecalho[i].replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')] = textos[i]
			dicionario[textos[0]] = item

	lista = list(dicionario.values())
	return json.dumps(lista, ensure_ascii=False, indent=3).encode('utf8')

@cross_origin()
@app.route('/api/resources/statusinvest/<nome_acao>')
def acao_statusinvest(nome_acao):
	return statusInvest.get_cotacao(nome_acao)


#Executa nossa aplicacao
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

