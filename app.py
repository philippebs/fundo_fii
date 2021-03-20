from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import acao, fii


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
@app.route("/api/resources/fii")
def fundo_fii():
	return fii.get_fiis()


@cross_origin()
@app.route('/api/resources/acao/<nome_acao>')
def fund_acao(nome_acao):
	return acao.get_cotacao(nome_acao)
	

#Executa nossa aplicacao
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

