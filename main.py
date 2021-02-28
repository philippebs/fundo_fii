from flask import Flask, render_template

#Inicializa nossa aplicacao Flask
app =  Flask(__name__)

#Cria a rota para o caminho
@app.route("/")
def index():
	return render_template('index.html')

#Executa nossa aplicacao
if __name__ == "__main__":
	app.run(debug=True, port=4000)

