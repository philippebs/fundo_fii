import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
import acao, fii
from database import db_session
import os

#Inicializa nossa aplicacao Flask
app =  Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def save_ip(ip):
	with open('ips.txt', 'a', encoding='utf-8') as txt_file:
		txt_file.write("{IP: " + ip + ' , Hora: ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '}\n')


#Cria a rota para o caminho
@app.route("/")
@cross_origin()
def index():
	return render_template('index.html')


@app.route("/api/resources/fii")
@cross_origin()
def fundo_fii():
	return fii.get_fiis()


@app.route("/api/v1/resources/fii")
@cross_origin()
def fundo_fii_v1():
	json_fii = fii.get_fiis_v1()
	return jsonify(json_fii)


@app.route('/api/v1/resources/fii/codigos')
@cross_origin()
def fund_fii_codes_v1():
	return jsonify(fii.get_fiis_codes())


@app.route("/api/v1/create/fii")
@cross_origin()
def create_fundo_fii_v1():
	fii.create_fiis()
	return jsonify({'success': True})


@app.route('/api/resources/acao/<nome_acao>')
@cross_origin()
def fund_acao(nome_acao):
	return acao.get_cotacao(nome_acao)


#Executa nossa aplicacao
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

