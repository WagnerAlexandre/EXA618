from flask import Flask, request, jsonify
import requests
import os, datetime

app = Flask(__name__)

# O Token   
BLOB_TOKEN = os.environ.get("vercel_blob_rw_mVnWxuxouhSW7D1h_onOCt4VBGTu2V89GjEc8VdpXLQXK5t")
# Nome do seu arquivo no storage
FILENAME = "dados.csv"
# storage URL base  
BASE_URL = "BLOB_READ_WRITE_TOKEN"

app = Flask(__name__)
from flask import Flask, request, jsonify
import requests
import os
import datetime

app = Flask(__name__)

BLOB_TOKEN = os.environ.get("BLOB_READ_WRITE_TOKEN")
BASE_URL = "https://mvnwxuxouhsw7d1h.public.blob.vercel-storage.com"
FILENAME = "dados.csv"

@app.route('/')
def home():
    return "API Online! Use o endpoint /salvar via POST."

@app.route('/salvar', methods=['POST'])
def salvar_dados():
    data_json = request.get_json()
    
    # Pegando dados do JSON
    nome = data_json.get('nome', 'N/A')
    mensagem = data_json.get('mensagem', 'Sem mensagem')
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_url = f"{BASE_URL}/{FILENAME}"
    
    try:    
        res = requests.get(file_url)

        if res.status_code == 200:
            conteudo_atual = res.text
        else:
            conteudo_atual = "Data,Nome,Mensagem\n"

        if not conteudo_atual.endswith('\n'):
            conteudo_atual += '\n'
            
        nova_linha = f"{agora},{nome},{mensagem}\n"
        novo_conteudo = conteudo_atual + nova_linha

        upload_url = f"https://blob.vercel-storage.com/{FILENAME}"
        headers = {
            "Authorization": f"Bearer {BLOB_TOKEN}",
            "x-api-version": "1",
            "Content-Type": "text/csv" 
        }
        
        put_res = requests.put(
            upload_url, 
            data=novo_conteudo.encode('utf-8'), 
            headers=headers,
            params={"addRandomSuffix": "false"}
        )

        if put_res.status_code == 200:
            return jsonify({"status": "sucesso", "url": file_url})
        return jsonify({"status": "erro", "detalhes": put_res.text}), 500

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

def handler(event, context):
    return app(event, context)

@app.route('/')
def home():
    return "API Online! Use o endpoint /salvar via POST."

@app.route('/salvar', methods=['POST'])
def salvar_dados():
    data = request.get_json()
    
    nome = data.get('nome', 'N/A')
    valor = data.get('mensagem', '0')
    data = datetime.datetime.now()


    file_url = f"{BASE_URL}/{FILENAME}"
    
    try:    
        res = requests.get(file_url)
        conteudo_atual = res.text if res.status_code == 200 else "Nome,Valor\n"

        novo_conteudo = conteudo_atual + f"{nome},{valor}\n"


        upload_url = f"https://blob.vercel-storage.com/{FILENAME}"
        headers = {
            "Authorization": f"Bearer {BLOB_TOKEN}",
            "x-api-version": "1"
        }
        

        put_res = requests.put(
            upload_url, 
            data=novo_conteudo.encode('utf-8'), 
            headers=headers,
            params={"addRandomSuffix": "false"}
        )

        if put_res.status_code == 200:
            return jsonify({"status": "sucesso", "url": file_url})
        return jsonify({"status": "erro", "detalhes": put_res.text}), 500

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route('/dados', methods=['GET'])
def recuperar_dados():
    file_url = f"{BASE_URL}/{FILENAME}"
    
    try:
        res = requests.get(file_url)
        
        if res.status_code != 200:
            return jsonify({"status": "erro", "mensagem": "Arquivo não encontrado ou vazio"}), 404

        import csv
        import io

        f = io.StringIO(res.text)
        reader = csv.DictReader(f)
        
        lista_dados = []
        for linha in reader:
            lista_dados.append(linha)

        return jsonify({
            "status": "sucesso",
            "quantidade": len(lista_dados),
            "dados": lista_dados
        }), 200

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

def handler(event, context):
    return app(event, context)