import socket
import threading

HOST = '127.0.0.1'
PORTA = 50000

clientes = []


def enviar_para_outros(cliente_socket, mensagem):
    """
    Envia uma mensagem para todos os clientes,
    exceto para quem enviou.
    """

    for cliente in clientes[:]:

        if cliente["socket"] != cliente_socket:

            try:
                # \n é usado para separar as mensagens
                cliente["socket"].send(
                    (mensagem + "\n").encode("utf-8")
                )

            except:
                sair(cliente["socket"])


def gerenciar_cliente(cliente_socket):

    nome_atual = ""

    # Descobre o nome do cliente
    for cliente in clientes:
        if cliente["socket"] == cliente_socket:
            nome_atual = cliente["nome"]
            break

    while True:

        try:

            mensagem = cliente_socket.recv(1024)

            if not mensagem:
                break

            mensagem = mensagem.decode("utf-8").strip()

            if mensagem:

                mensagem_formatada = (
                    f"[{nome_atual}]: {mensagem}"
                )

                print(mensagem_formatada)

                enviar_para_outros(
                    cliente_socket,
                    mensagem_formatada
                )

        except:

            break

    sair(cliente_socket)


def sair(cliente_socket):

    for cliente in clientes[:]:

        if cliente["socket"] == cliente_socket:

            print(
                f"[DESCONECTADO] "
                f"{cliente['nome']} saiu do chat."
            )

            clientes.remove(cliente)

            try:
                cliente_socket.close()
            except:
                pass

            break


def iniciar_servidor():

    servidor = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    servidor.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    servidor.bind(
        (HOST, PORTA)
    )

    servidor.listen(2)

    print(
        f"Servidor iniciado em "
        f"{HOST}:{PORTA}"
    )

    print(
        "Aguardando até 2 pessoas..."
    )

    while True:

        if len(clientes) < 2:

            cliente_socket, endereco = servidor.accept()

            # Solicita o nome
            cliente_socket.send(
                "SOLICITAR_NOME".encode("utf-8")
            )

            nome = cliente_socket.recv(
                1024
            ).decode("utf-8").strip()

            if not nome:
                nome = "Anônimo"

            clientes.append({
                "socket": cliente_socket,
                "nome": nome
            })

            print(
                f"[CONEXÃO] {nome} "
                f"({endereco}) entrou na sala. "
                f"({len(clientes)}/2)"
            )

            thread = threading.Thread(
                target=gerenciar_cliente,
                args=(cliente_socket,)
            )

            thread.daemon = True
            thread.start()


if __name__ == "__main__":
    iniciar_servidor()