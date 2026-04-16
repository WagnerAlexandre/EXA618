from flask import Flask, request, jsonify
import requests
import os, csv, io
import datetime

app = Flask(__name__)


BLOB_TOKEN = os.environ.get("BLOB_READ_WRITE_TOKEN")
BASE_URL = "https://mvnwxuxouhsw7d1h.public.blob.vercel-storage.com"
FILENAME = "dados.csv"



@app.route('/atividade7')
def home():
    return "API Atividade 7 Online!"

@app.route('/atividade7/enviar', methods=['PUT'])
def enviar():

    novo_conteudo = request.data 
    

    headers = {
        "Authorization": f"Bearer {BLOB_TOKEN}",
        "x-api-version": "1",
        "Content-Type": "text/csv"
    }
    
    params = {"addRandomSuffix": "false"}
    

    target_url = f"https://blob.vercel-storage.com/{FILENAME}"
    
    try:

        response = requests.put(
            target_url, 
            data=novo_conteudo, 
            headers=headers, 
            params=params
        )
        
        if response.status_code == 200:
            return jsonify({"status": "sucesso", "url": response.json().get('url')}), 200
        else:
            return jsonify({"status": "erro", "detalhes": response.text}), response.status_code
            
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route('/atividade7/salvar', methods=['POST'])
def salvar():
    data_json = request.get_json()
    usuario = data_json.get('usuario', 'Anônimo')
    msg = data_json.get('mensagem', '')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_url = f"{BASE_URL}/{FILENAME}"
    
    try:
        res = requests.get(file_url)
        conteudo = res.text if res.status_code == 200 else "Data,Usuario,Mensagem\n"
        novo_conteudo = conteudo + f"{timestamp},{usuario},{msg}\n"

        headers = {
            "Authorization": f"Bearer {BLOB_TOKEN}",
            "x-api-version": "1"
        }
        
        requests.put(
            f"https://blob.vercel-storage.com/{FILENAME}",
            data=novo_conteudo.encode('utf-8'),
            headers=headers,
            params={"addRandomSuffix": "false"}
        )
        return jsonify({"status": "sucesso"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/atividade7/mensagens', methods=['GET'])
def listar():
    file_url = f"{BASE_URL}/{FILENAME}"
    try:
        res = requests.get(file_url)
        if res.status_code != 200: return jsonify({"mensagens": []})
        f = io.StringIO(res.text)
        reader = csv.DictReader(f)
        return jsonify({"mensagens": list(reader)})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
