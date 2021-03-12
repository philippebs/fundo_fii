import requests
from bs4 import BeautifulSoup
import json

class Acao:
	
	def __init__(self, nome, descricao, tipo, valor):
		self.nome = nome
		self.descricao = descricao.replace('\n', '')[0:15]
		self.tipo = tipo
		self.valor = valor


	def __str__(self):
		descricao_retorno = self.descricao
		if len(self.descricao) > 15:
			descricao_retorno = self.descricao[0:15]

		return self.nome + ' - ' + descricao_retorno + ' - ' + self.tipo + ' - ' + self.valor


	def toJSON(self):
		return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def get_cotacao(nome_acao):
	lista = []
	headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
	url = 'https://statusinvest.com.br/acoes/%s' % nome_acao
	response = requests.get(url, headers=headers, timeout=10)
	soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

	div_info = soup.find('div', attrs={'class': 'top-info'})

	for info in div_info.find_all('div', attrs={'class': 'info'}):
		descricao = info.find('h3', attrs={'class': 'title m-0'})
		tipo =  info.find('span', attrs={'class': 'icon'})
		valor = info.find('strong', attrs={'class': 'value'})
		if descricao is None:
			descricao = info.find('h3', attrs={'class': 'title m-0 legend-tooltip'})


		acao = Acao(nome_acao, descricao.text, tipo.text, valor.text)
		lista.append(acao)
	
	return json.dumps(lista, ensure_ascii=False, default=lambda o: o.__dict__, indent=3)


if __name__ == "__main__":
	print(get_cotacao('petr4'))
	# get_cotacao('cvcb3')