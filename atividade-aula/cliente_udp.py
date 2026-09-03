import socket
import sys

HOST = "127.0.0.1"
PORT = 5001
MATRICULA = "#"
EMAIL = "#"

payload = f"{MATRICULA},{EMAIL}"

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(5.0)
        client_socket.sendto(payload.encode("utf-8"), (HOST, PORT))
        
        dados, _ = client_socket.recvfrom(1024)
        resposta = dados.decode("utf-8").strip()

    if resposta == "OK":
        sys.exit(0)
    else:
        sys.exit(1)

except Exception:
    sys.exit(1)