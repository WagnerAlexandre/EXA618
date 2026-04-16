import requests
import os, csv, io
import datetime
import json

# Configurações
BLOB_TOKEN = os.environ.get("BLOB_READ_WRITE_TOKEN")
BASE_URL = "https://mvnwxuxouhsw7d1h.public.blob.vercel-storage.com"
FILENAME = "dados.csv"

def app(environ, start_response):
    # Pega o caminho da URL e o método (GET, POST, etc)
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', 'GET')

    # Rota: /api/atividade7/mensagens
    if path == '/api/atividade7/mensagens' and method == 'GET':
        file_url = f"{BASE_URL}/{FILENAME}"
        try:
            res = requests.get(file_url)
            status = '200 OK'
            if res.status_code != 200:
                response_body = json.dumps({"mensagens": []})
            else:
                f = io.StringIO(res.text)
                reader = csv.DictReader(f)
                response_body = json.dumps({"mensagens": list(reader)})
        except Exception as e:
            status = '500 Internal Server Error'
            response_body = json.dumps({"erro": str(e)})

    # Rota: /api/atividade7 (Simples teste)
    elif path == '/api/atividade7':
        status = '200 OK'
        response_body = "API Atividade 7 Online (Sem Flask)!"
    
    # Rota: /api/atividade7/salvar
    elif path == '/api/atividade7/salvar' and method == 'POST':
        try:
            # Lendo o corpo do POST
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            data_json = json.loads(request_body)
            
            usuario = data_json.get('usuario', 'Anônimo')
            msg = data_json.get('mensagem', '')
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  
            res = requests.get(f"{BASE_URL}/{FILENAME}")
            conteudo = res.text if res.status_code == 200 else "Data,Usuario,Mensagem\n"
            novo_conteudo = conteudo + f"{timestamp},{usuario},{msg}\n"


            requests.put(
                f"https://blob.vercel-storage.com/{FILENAME}",
                data=novo_conteudo.encode('utf-8'),
                headers={"Authorization": f"Bearer {BLOB_TOKEN}", "x-api-version": "1"},
                params={"addRandomSuffix": "false"}
            )
            status = '200 OK'
            response_body = json.dumps({"status": "sucesso"})
        except Exception as e:
            status = '500 Internal Server Error'
            response_body = json.dumps({"erro": str(e)})

    else:
        status = '404 Not Found'
        response_body = json.dumps({"erro": "Rota nao encontrada", "path": path})

    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]