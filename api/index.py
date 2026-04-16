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
            file_url = f"{BASE_URL}/{FILENAME}"

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



    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data_json = json.loads(post_data)

            usuario = data_json.get('usuario', 'Anônimo')
            msg = data_json.get('mensagem', '')
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 1. Busca o CSV atual - Adicionamos um parâmetro aleatório para evitar cache na leitura
            res = requests.get(f"{BASE_URL}/{FILENAME}?t={datetime.datetime.now().timestamp()}")
            
            if res.status_code == 200:
                conteudo = res.text
                # Garante que o arquivo termina com quebra de linha antes de adicionar nova
                if conteudo and not conteudo.endswith('\n'):
                    conteudo += '\n'
            else:
                conteudo = "Data,Usuario,Mensagem\n"

            novo_conteudo = conteudo + f"{timestamp},{usuario},{msg}\n"

            # 2. Upload para o Vercel Blob
            # Verifique se o BLOB_TOKEN está realmente carregado
            if not BLOB_TOKEN:
                 raise Exception("BLOB_READ_WRITE_TOKEN não configurada")

            upload_url = f"https://blob.vercel-storage.com/{FILENAME}"
            
            blob_res = requests.put(
                upload_url,
                data=novo_conteudo.encode('utf-8'),
                headers={
                    "Authorization": f"Bearer {BLOB_TOKEN}",
                    "x-api-version": "1",
                    "x-add-random-suffix": "false", # Algumas versões usam header em vez de params
                    "Content-Type": "text/csv"
                },
                params={"addRandomSuffix": "false"}
            )

            if blob_res.status_code not in [200, 201]:
                raise Exception(f"Erro no Blob: {blob_res.text}")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "sucesso", "arquivo": FILENAME}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "erro", "detalhes": str(e)}).encode('utf-8'))



    def enviar_erro(self, mensagem, código=500):
        self.send_response(código)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"erro": mensagem}).encode('utf-8'))