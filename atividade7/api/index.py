from http.server import BaseHTTPRequestHandler
import requests
import os
import json
import io
import csv
import datetime

# Configurações do Vercel Blob
BLOB_TOKEN = os.environ.get("BLOB_READ_WRITE_TOKEN")
BASE_URL = "https://mvnwxuxouhsw7d1h.public.blob.vercel-storage.com"
FILENAME = "dados.csv"

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Rota: /api/atividade7/mensagens
        if self.path == '/api/atividade7/mensagens':
            file_url = f"{BASE_URL}/{FILENAME}"
            try:
                res = requests.get(file_url)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                if res.status_code != 200:
                    response = {"mensagens": []}
                else:
                    f = io.StringIO(res.text)
                    reader = csv.DictReader(f)
                    response = {"mensagens": list(reader)}
                
                self.wfile.write(json.dumps(response).encode('utf-8'))

            except Exception as e:
                self.enviar_erro(str(e))

        # Rota: /api/atividade7
        elif self.path == '/api/atividade7':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("API Atividade 7 Online (BaseHTTPRequestHandler)!".encode('utf-8'))
        
        else:
            self.enviar_erro("Rota nao encontrada", 404)

    def do_POST(self):
        # Rota: /api/atividade7/salvar
        if self.path == '/api/atividade7/salvar':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data_json = json.loads(post_data)

                usuario = data_json.get('usuario', 'Anônimo')
                msg = data_json.get('mensagem', '')
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 1. Busca conteúdo atual
                res = requests.get(f"{BASE_URL}/{FILENAME}")
                conteudo = res.text if res.status_code == 200 else "Data,Usuario,Mensagem\n"
                
                # 2. Prepara novo CSV
                novo_conteudo = conteudo + f"{timestamp},{usuario},{msg}\n"

                # 3. Envia para o Blob
                blob_res = requests.put(
                    f"https://blob.vercel-storage.com/{FILENAME}",
                    data=novo_conteudo.encode('utf-8'),
                    headers={
                        "Authorization": f"Bearer {BLOB_TOKEN}",
                        "x-api-version": "1"
                    },
                    params={"addRandomSuffix": "false"}
                )

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "sucesso"}).encode('utf-8'))

            except Exception as e:
                self.enviar_erro(str(e))
        else:
            self.enviar_erro("Rota nao encontrada", 404)

    def enviar_erro(self, mensagem, código=500):
        self.send_response(código)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"erro": mensagem}).encode('utf-8'))