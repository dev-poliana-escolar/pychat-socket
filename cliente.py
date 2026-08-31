import socket
import threading
import sys

# IP do servidor
HOST = '127.0.0.1'
PORTA = 50000


def receber_mensagens(cliente_socket):
    """Fica aguardando mensagens enviadas pelo servidor."""

    while True:
        try:
            mensagem = cliente_socket.recv(1024).decode('utf-8')

            if not mensagem:
                print("\n[INFO] O servidor encerrou a conexão.")
                break

            # Mostra a mensagem recebida
            print(mensagem, end='', flush=True)

        except:
            print("\n[INFO] Conexão com o servidor perdida.")
            break

    cliente_socket.close()
    sys.exit()


def iniciar_cliente():

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente_socket.connect((HOST, PORTA))

    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor.")
        print(f"[INFO] Verifique se o servidor está rodando em {HOST}:{PORTA}")
        return

    except Exception as erro:
        print(f"[ERRO] Falha na conexão: {erro}")
        return

    print(f"[CONECTADO] Servidor {HOST}:{PORTA}")

    # Aguarda o servidor solicitar o nome
    resposta = cliente_socket.recv(1024).decode('utf-8')

    if resposta == "SOLICITAR_NOME":

        nome = input("Digite seu nome: ").strip()

        if not nome:
            nome = "Anônimo"

        cliente_socket.send(nome.encode('utf-8'))

    # Cria uma thread para receber mensagens
    thread_receber = threading.Thread(
        target=receber_mensagens,
        args=(cliente_socket,)
    )

    thread_receber.daemon = True
    thread_receber.start()

    print("\n================================")
    print("       CHAT INICIADO")
    print("================================")
    print("Digite sua mensagem e pressione ENTER.")
    print("Use CTRL+C para sair.")
    print("================================\n")

    try:
        while True:

            mensagem = input("[Você]: ")

            if mensagem.strip():

                cliente_socket.send(
                    mensagem.encode('utf-8')
                )

    except KeyboardInterrupt:
        print("\n\n[INFO] Saindo do chat...")

    except Exception as erro:
        print(f"\n[ERRO] {erro}")

    finally:
        cliente_socket.close()


if __name__ == "__main__":
    iniciar_cliente()