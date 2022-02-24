import requests
from bs4 import BeautifulSoup
import json
from unicodedata import normalize
import re
from models import AcaoOld

# class Acao:
	
# 	def __init__(self, nome, descricao, tipo, valor):
# 		self.nome = nome
# 		self.descricao = self.remover_caracter_special(self.normalizar_string(descricao))[0:20]
# 		self.tipo = tipo
# 		self.valor = valor


# 	def normalizar_string(self, texto):
# 		return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')


# 	def remover_caracter_special(self, texto):
# 		return re.sub('[/!@#$().\n]', '', texto)

# 	def __str__(self):
# 		descricao_retorno = self.descricao
# 		if len(self.descricao) > 15:
# 			descricao_retorno = self.descricao[0:15]

# 		return self.nome + ' - ' + descricao_retorno + ' - ' + self.tipo + ' - ' + self.valor


# 	def toJSON(self):
# 		return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def get_cotacao(nome_acao):
	lista = []
	headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
	url = 'https://statusinvest.com.br/acoes/%s' % nome_acao
	response = requests.get(url, headers=headers, timeout=10)
	soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
	valor_atual = soup.select('#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div.info.special.w-100.w-md-33.w-lg-20 > div > div:nth-child(1) > strong')[0].text
	min_52_semanas = soup.select('#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(2) > div > div:nth-child(1) > strong')[0].text
	max_52_semanas = soup.select('#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(3) > div > div:nth-child(1) > strong')[0].text
	dividend_yield = soup.select('#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(4) > div > div:nth-child(1) > strong')[0].text
	valorizacao_12m = soup.select('#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(5) > div > div:nth-child(1) > strong')[0].text
	dy = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(1) > div > div > strong')[0].text
	pl = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(2) > div > div > strong')[0].text
	peg_ratio = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(3) > div > div > strong')[0].text
	pvp = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(4) > div > div > strong')[0].text 
	evebitda = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(5) > div > div > strong')[0].text
	evebit = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(8) > div > div > strong')[0].text
	pebitda = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(7) > div > div > strong')[0].text
	pebit = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(8) > div > div > strong')[0].text
	vpa = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(9) > div > div > strong')[0].text
	pativo = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(10) > div > div > strong')[0].text
	lpa = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(11) > div > div > strong')[0].text
	psr = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(12) > div > div > strong')[0].text
	pcap_giro = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(13) > div > div > strong')[0].text
	pativo_circ_liq = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(14) > div > div > strong')[0].text
	div_liquidapl = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(2) > div > div:nth-child(1) > div > div > strong')[0].text
	div_liquidaebitda = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(2) > div > div:nth-child(2) > div > div > strong')[0].text
	div_liquidaebit = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(2) > div > div:nth-child(3) > div > div > strong')[0].text
	plativos = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(2) > div > div:nth-child(4) > div > div > strong')[0].text
	passivoativos = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(2) > div > div:nth-child(5) > div > div > strong')[0].text
	liq_corrente = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(2) > div > div:nth-child(6) > div > div > strong')[0].text
	m_bruta = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(3) > div > div:nth-child(1) > div > div > strong')[0].text
	m_ebitda = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(3) > div > div:nth-child(2) > div > div > strong')[0].text
	m_ebit = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(3) > div > div:nth-child(3) > div > div > strong')[0].text
	m_liquida = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(3) > div > div:nth-child(4) > div > div > strong')[0].text
	roe = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(4) > div > div:nth-child(1) > div > div > strong')[0].text
	roa = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(4) > div > div:nth-child(2) > div > div > strong')[0].text
	roic = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(4) > div > div:nth-child(3) > div > div > strong')[0].text
	giro_ativos = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(4) > div > div:nth-child(4) > div > div > strong')[0].text
	cagr_receitas_5_anos = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(5) > div > div:nth-child(1) > div > div > strong')[0].text
	cagr_lucros_5_anos = soup.select('#indicators-section > div.indicator-today-container > div > div:nth-child(5) > div > div:nth-child(2) > div > div > strong')[0].text
	
	acao = AcaoOld(nome_acao, valor_atual, min_52_semanas, max_52_semanas, dividend_yield, valorizacao_12m, dy, pl, peg_ratio, pvp, evebitda, evebit, pebitda, pebit, vpa,
				pativo, lpa, psr, 	pcap_giro, pativo_circ_liq, div_liquidapl, div_liquidaebitda, div_liquidaebit, plativos, passivoativos, liq_corrente, m_bruta,
				m_ebitda, m_ebit, m_liquida, roe, roa, roic, giro_ativos, cagr_receitas_5_anos, cagr_lucros_5_anos)
	return json.dumps(acao, ensure_ascii=False, default=lambda o: o.__dict__, indent=3)
	# div_info = soup.find('div', attrs={'class': 'top-info'})

	# for info in div_info.find_all('div', attrs={'class': 'info'}):
	# 	descricao = info.find('h3', attrs={'class': 'title m-0'})
	# 	tipo =  info.find('span', attrs={'class': 'icon'})
	# 	valor = info.find('strong', attrs={'class': 'value'})
	# 	if descricao is None:
	# 		descricao = info.find('h3', attrs={'class': 'title m-0 legend-tooltip'})


	# 	acao = Acao(nome_acao, descricao.text, tipo.text, valor.text)
	# 	lista.append(acao)
	
	# historico = soup.find('div', attrs={'class': 'today-historical-container'})
	# indicadores = historico.find_all('div', attrs={'class': 'indicators'})
	# for indicador in indicadores:
	# 	tipo_indicador = indicador.find('strong', attrs={'d-block uppercase'})
	# 	items = indicador.find_all('div', attrs={'item'})
	# 	for item in items:
	# 		titulo = item.find('h3', attrs={'class': 'title'})
	# 		valor = item.find('strong', attrs={'class': 'value'})
	# 		tipo = 'R$'
	# 		if '%' not in valor.text:
	# 			tipo = '%'
	# 		acao = Acao(nome_acao, titulo.text, tipo, valor.text)
	# 		lista.append(acao)
	# return json.dumps(acao, ensure_ascii=False, default=lambda o: o.__dict__, indent=3)


if __name__ == "__main__":
	print(get_cotacao('petr4'))
	# get_cotacao('petr4')
	# get_cotacao('cvcb3')