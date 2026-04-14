#!/usr/bin/env python3
import os, csv, datetime, sys, io
from urllib.parse import parse_qs

qs = os.environ["QUERY_STRING"]
list = parse_qs(qs, encoding="utf-8")
nome = list["nome"][0]
mensagem = list["mensagem"][0]
data = datetime.datetime.today()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

msg = {
    'nome' : nome,
    'data' : data,
    'mensagem' : mensagem

    }

arquivo_existe = os.path.exists('database.csv')
arquivo_vazio = not arquivo_existe or os.stat('database.csv').st_size == 0
colunas = ['nome','data','mensagem',]

with open('database.csv','a+',encoding='utf-8',newline='') as file:
    reader = csv.DictReader(file,fieldnames=colunas)
    writer = csv.DictWriter(f=file,fieldnames=colunas)
    if arquivo_vazio:
        writer.writeheader()
    writer.writerow(msg)
    pass

print("Content-type: text/html;charset=utf-8")
print()

print('<html>')
print('<head><title>Exemplo GET</title>')
print('  <meta charset="utf-8">')
print('</head>')
print('<body>')
print('<h1> "NOSSO" diario!</h1>')
print('  <form method="GET" action="http://localhost:8000/cgi-bin/get.py">')
print('    <p> Nome: <input type="text" size="15" name="nome"></p>')
print('    <p>Mensagem: <input type="text" size="45" name ="mensagem" ></p>')
print('    <input type="submit">')
print('  </form>')


with open('database.csv','r',encoding='utf-8',newline='') as file:
    reader = csv.DictReader(file)
    lista = []
    for i in reader:
        lista.append((i['nome'],i['data'],i['mensagem']))
    pass
    lista.sort(key=lambda x:x[1], reverse=True)
    for i in lista:
        print("<hr>")
        print("nome = '" + i[0] + "'<br>")
        print("Data = '" + i[1] + "'<br>")
        print("mensagem = '" + i[2] + "'<br>")
        print("</body></html>")
        pass
print('</body></html>')

