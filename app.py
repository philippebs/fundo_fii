from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

#Inicializa nossa aplicacao Flask
app =  Flask(__name__)

#Cria a rota para o caminho
@app.route("/")
def index():
	headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
	url = 'https://www.fundsexplorer.com.br/ranking'
	response = requests.get(url, headers=headers, timeout=10)
	return render_template('index.html')

#Executa nossa aplicacao
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

