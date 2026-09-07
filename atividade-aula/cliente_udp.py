import socket
import sys

HOST = "127.0.0.1"
PORT = 5000
payload = "2025000,p@escolar.edu.br"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.sendto(payload.encode(), (HOST, PORT))
    resposta, _ = sock.recvfrom(1024)

resposta = resposta.decode()
print(resposta)

sys.exit(0 if resposta == "OK" else 1)