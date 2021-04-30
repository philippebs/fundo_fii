from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
import acao, fii


#Inicializa nossa aplicacao Flask
app =  Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def save_ip(ip):
	with open('ips.txt', 'a', encoding='utf-8') as txt_file:
		txt_file.write("{IP: " + ip + ' , Hora: ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '}\n')

#Cria a rota para o caminho
@app.route("/")
@cross_origin()
def index():
	save_ip(request.remote_addr)
	return render_template('index.html')


@app.route("/api/resources/fii")
@cross_origin()
def fundo_fii():
	return fii.get_fiis()


@app.route('/api/resources/acao/<nome_acao>')
@cross_origin()
def fund_acao(nome_acao):
	return acao.get_cotacao(nome_acao)
	

#Executa nossa aplicacao
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

