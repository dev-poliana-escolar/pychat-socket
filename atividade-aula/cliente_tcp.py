import socket
import sys

HOST = "127.0.0.1"
PORT = 5000
payload = "2025000,p@escolar.edu.br"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.sendall(payload.encode())

    resposta = sock.recv(1024).decode()
    print(resposta)

    if resposta == "ERRO":
        sys.exit(1)

    while True:
        matricula = input("Matrícula (0 para sair): ")
        sock.sendall(matricula.encode())

        if matricula == "0":
            break
        print(sock.recv(1024).decode())

sys.exit(0)