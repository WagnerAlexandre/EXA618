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
        # Rota principal pedida: /api/index
        if self.path == '/api/index':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("API Atividade 7 via /api/index está Online!".encode('utf-8'))

        # Rota de listagem: /api/index/mensagens ou /api/atividade7/mensagens
        elif '/mensagens' in self.path:
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
        
        else:
            self.enviar_erro(f"Rota {self.path} nao encontrada", 404)

    def do_POST(self):
        # Rota de salvamento
        if '/salvar' in self.path:
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data_json = json.loads(post_data)

                usuario = data_json.get('usuario', 'Anônimo')
                msg = data_json.get('mensagem', '')
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Busca o CSV atual para anexar
                res = requests.get(f"{BASE_URL}/{FILENAME}")
                conteudo = res.text if res.status_code == 200 else "Data,Usuario,Mensagem\n"
                novo_conteudo = conteudo + f"{timestamp},{usuario},{msg}\n"

                # Upload para o Vercel Blob
                requests.put(
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
            self.enviar_erro("Rota de postagem nao encontrada", 404)

    def enviar_erro(self, mensagem, código=500):
        self.send_response(código)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"erro": mensagem}).encode('utf-8'))