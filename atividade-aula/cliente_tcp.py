import socket
import sys

HOST = "127.0.0.1"
PORT = 5000
MATRICULA = "#"
EMAIL = "#"

payload = f"{MATRICULA},{EMAIL}"

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.settimeout(5.0)
        client_socket.connect((HOST, PORT))
        client_socket.sendall(payload.encode("utf-8"))
        
        resposta = client_socket.recv(1024).decode("utf-8").strip()

    if resposta == "OK":
        sys.exit(0)
    else:
        sys.exit(1)

except Exception:
    sys.exit(1)