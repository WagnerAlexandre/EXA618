#!/usr/bin/env python3

import os, datetime, cgi,csv
import sys
from urllib.parse import parse_qs

content_length = int(os.environ.get("CONTENT_LENGTH", 0))
body = sys.stdin.buffer.read(content_length).decode('utf-8')

params = parse_qs(body, encoding="utf-8")

nome = params.get("nome", [""])[0]

print("Content-Type: text/html; charset=utf-8")
print()
print("<html><head><title>Post Example</title></head><body>")
print("Nome: " + nome + "<br>")
print("CONTENT_LENGTH=" + os.environ.get("CONTENT_LENGTH", "0") + "<br>")
print("</body></html>")


form = cgi.FieldStorage()

resp = {'nome': str(form.getvalue('nome')),
        'data': datetime.date.today(),
        'mensagem': str(form.getvalue('mensagem'))
        }

csv_path = 'database.csv'
colunas = ['nome', 'data', 'mensagem']

with open(csv_path, 'a', encoding='UTF-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=colunas)
    if os.path.exists(csv_path) and os.stat(csv_path).st_size == 0:
        writer.writeheader()
        
    writer.writerow(resp)

print ("Content-type: text/html; charset=utf-8")
print ()
print ("<html><head><title>Post Example</title></head><body>")
print (f"Nome:{resp['nome']} <br>")
print (f"Mensagem: {resp['mensagem']} <br>")
print (f"Data: {str(resp['data'])} <br>")
print ("</body></html>")

