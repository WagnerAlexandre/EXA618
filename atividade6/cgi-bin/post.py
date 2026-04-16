#!/usr/bin/env python3

import os
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