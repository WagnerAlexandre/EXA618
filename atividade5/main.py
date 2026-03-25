from bs4 import BeautifulSoup as BS
from urllib import request


page = request.urlopen('https://exa-618-xi.vercel.app/atividade1')
html = str(page.read().decode('utf-8'))
soup = BS(html, 'html.parser')
print("Título:", soup.title.string)
for img in soup.find_all('img'):
    print("src: ", img.attrs.get("src"))

colecao = []

with open("atividade5/seeds.txt","r", encoding="UTF-8") as seeds:
    
    for pageS in seeds:
        page = request.urlopen(pageS)
        html = str(page.read().decode('utf-8'))
        soup = BS(html, 'html.parser')  
        titulo = soup.title.string
        print("Entrando no link:",pageS)
        print("Referente:",titulo)

        imgs = []
        for img in soup.find_all('img'):
            link = img.attrs.get("src")
            if 'https'in link or 'data:image' in link:
                colecao.append([titulo,img.attrs.get("src")])
                break
            else:

                link = link.replace("./","").replace("../","").replace(".../","").replace("//","").replace("/.","").replace("/atividade1","")
                link = pageS.replace("index.html","")+'/'+link

                colecao.append([titulo,link])
                break

message = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scrapped Pages</title>
</head>
<body>
"""
for i in colecao:
   message += f"""
   <h1>{i[0]}</h1>
   <img src="{i[1]}"> </div>
    """
message += "</body> </html>"


with open("atividade5/index.html", "w", encoding='utf-8') as f:
    f.write(message)
