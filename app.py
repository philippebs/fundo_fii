from flask import Flask, render_template

#Inicializa nossa aplicacao Flask
app =  Flask(__name__)

#Cria a rota para o caminho
@app.route("/")
def index():
	return render_template('index.html')

#Executa nossa aplicacao
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

