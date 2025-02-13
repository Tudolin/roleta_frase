from flask import Flask, render_template, request, jsonify
import random
import json
from datetime import datetime

app = Flask(__name__)

# Listas para gerar frases
inicios = ["E aí", "Oi", "Bom dia", "Fala", "Opa"]
publicos = ["pessoal", "gente", "time", "galera", "turma", "equipe"]
complementos = [
   "tudo certo?",
   "vamos nessa!",
   "bora lá!",
   "como estão?",
   "espero que estejam bem!",
   "prontos para começar?",
   "tudo tranquilo por aí?",
   "bora pra mais um dia!"
]

# Caminho do arquivo JSON para armazenar os logs
LOG_FILE = "logs.json"

# Função para carregar os logs do arquivo JSON
def load_logs():
   try:
       with open(LOG_FILE, "r") as file:
           return json.load(file)
   except FileNotFoundError:
       return []

# Função para salvar os logs no arquivo JSON
def save_logs(logs):
   with open(LOG_FILE, "w") as file:
       json.dump(logs, file, indent=4)

@app.route("/")
def index():
   # Carrega os logs existentes
   logs = load_logs()
   return render_template("index.html", inicios=inicios, publicos=publicos, complementos=complementos, logs=logs)

@app.route("/log", methods=["POST"])
def log():
   data = request.json
   nome = data.get("nome")
   frase = data.get("frase")
   timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

   # Cria o novo log
   novo_log = {
       "nome": nome,
       "frase": frase,
       "data": timestamp
   }

   # Carrega os logs existentes, adiciona o novo log e salva
   logs = load_logs()
   logs.append(novo_log)
   save_logs(logs)

   return jsonify({"status": "success", "log": novo_log})

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0")
