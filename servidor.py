import socket
import threading

# comandos para conexao remota (hostname -I ou ifconfig)
HOST = '127.0.0.1' # aqui é meu localhost. Aqui se coloca o IP do servidor, quando for remoto.
PORTA = 50000

clientes = []

def gerenciar_cliente(cliente_socket):
    nome_atual = ""
    for c in clientes:
        if c["socket"] == cliente_socket:
            nome_atual = c["nome"]

    while True:
        try:
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            if not mensagem:
                break
            
            # envia a mensagem para o OUTRO cliente
            for c in clientes:
                if c["socket"] != cliente_socket:
                    try:
                        c["socket"].send(f"\n[{nome_atual}]: {mensagem}\n[Você]: ".encode('utf-8'))
                    except:
                        sair(c["socket"])
        except:
            break

    sair(cliente_socket)

def sair(cliente_socket):
    for c in clientes:
        if c["socket"] == cliente_socket:
            print(f"[DESCONECTADO] {c['nome']} saiu do chat.")
            clientes.remove(c)
            cliente_socket.close()
            break

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORTA))
    servidor.listen(2)
    print(f"Servidor iniciado em {HOST}:{PORTA}. Aguardando até 2 pessoas...")

    while True:
        if len(clientes) < 2:
            cliente_socket, endereco = servidor.accept()
            
            # pede o nome do cliente
            cliente_socket.send("SOLICITAR_NOME".encode('utf-8'))
            nome = cliente_socket.recv(1024).decode('utf-8')
            
            clientes.append({"socket": cliente_socket, "nome": nome})
            print(f"[CONEXÃO] {nome} ({endereco}) entrou na sala. ({len(clientes)}/2)")

            thread = threading.Thread(target=gerenciar_cliente, args=(cliente_socket,))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    iniciar_servidor()
