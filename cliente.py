import socket
import curses
import threading
import sys


HOST = '127.0.0.1'
PORTA = 50000


class Chat:

    def __init__(self, tela, cliente_socket):

        self.tela = tela
        self.socket = cliente_socket

        self.mensagens = []
        self.mensagem_atual = ""

        self.executando = True

        # Configurações do curses
        curses.curs_set(1)
        self.tela.nodelay(False)

        # Thread para receber mensagens
        self.thread = threading.Thread(
            target=self.receber_mensagens
        )

        self.thread.daemon = True
        self.thread.start()

    def receber_mensagens(self):

        """
        Recebe mensagens enviadas pelo servidor.
        """

        while self.executando:

            try:

                dados = self.socket.recv(1024)

                if not dados:
                    self.executando = False
                    break

                texto = dados.decode("utf-8")

                # Separa as mensagens pelo \n
                mensagens = texto.split("\n")

                for mensagem in mensagens:

                    mensagem = mensagem.strip()

                    if mensagem:
                        self.mensagens.append(
                            mensagem
                        )

                # Mantém somente as últimas 100 mensagens
                self.mensagens = self.mensagens[-100:]

                self.desenhar()

            except:

                self.executando = False
                break

    def desenhar(self):

        """
        Redesenha a tela do chat.
        """

        try:

            self.tela.erase()

            altura, largura = self.tela.getmaxyx()

            # Reserva as últimas duas linhas:
            # uma para a divisão e outra para digitação
            area_mensagens = altura - 2

            # Pega somente as mensagens que cabem na tela
            mensagens_visiveis = self.mensagens[
                -area_mensagens:
            ]

            # Exibe as mensagens
            for i, mensagem in enumerate(
                mensagens_visiveis
            ):

                mensagem = mensagem[:largura - 1]

                self.tela.addstr(
                    i,
                    0,
                    mensagem
                )

            # Linha divisória
            self.tela.addstr(
                altura - 2,
                0,
                "-" * (largura - 1)
            )

            # Prompt
            prompt = "[Você]: "

            texto = (
                prompt +
                self.mensagem_atual
            )

            texto = texto[:largura - 1]

            self.tela.addstr(
                altura - 1,
                0,
                texto
            )

            # Posiciona o cursor depois do texto digitado
            cursor_x = (
                len(prompt) +
                len(self.mensagem_atual)
            )

            cursor_x = min(
                cursor_x,
                largura - 1
            )

            self.tela.move(
                altura - 1,
                cursor_x
            )

            self.tela.refresh()

        except curses.error:

            pass

    def executar(self):

        """
        Controla a digitação do usuário.
        """

        self.desenhar()

        while self.executando:

            try:

                tecla = self.tela.getch()

                # ==========================
                # ENTER
                # ==========================
                if tecla in (
                    curses.KEY_ENTER,
                    10,
                    13
                ):

                    mensagem = (
                        self.mensagem_atual
                        .strip()
                    )

                    if mensagem:

                        # Mostra a própria mensagem
                        # imediatamente no chat
                        self.mensagens.append(
                            f"[Você]: {mensagem}"
                        )

                        # Mantém somente as últimas
                        # 100 mensagens
                        self.mensagens = (
                            self.mensagens[-100:]
                        )

                        # Atualiza a tela para
                        # mostrar a mensagem
                        self.desenhar()

                        try:

                            # Envia a mensagem
                            # para o servidor
                            self.socket.send(
                                mensagem.encode(
                                    "utf-8"
                                )
                            )

                        except:

                            self.executando = False
                            break

                    # Limpa o campo de texto
                    self.mensagem_atual = ""

                    self.desenhar()

                # ==========================
                # BACKSPACE
                # ==========================
                elif tecla in (
                    curses.KEY_BACKSPACE,
                    127,
                    8
                ):

                    if self.mensagem_atual:

                        self.mensagem_atual = (
                            self.mensagem_atual[:-1]
                        )

                    self.desenhar()

                # ==========================
                # CTRL + C
                # ==========================
                elif tecla == 3:

                    self.executando = False
                    break

                # ==========================
                # TECLAS NORMAIS
                # ==========================
                elif 32 <= tecla <= 126:

                    self.mensagem_atual += chr(
                        tecla
                    )

                    self.desenhar()

            except KeyboardInterrupt:

                self.executando = False
                break

            except:

                self.executando = False
                break

        # Fecha o socket
        try:
            self.socket.close()
        except:
            pass


def iniciar_cliente():

    # Cria o socket
    cliente_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # ==========================
    # CONEXÃO
    # ==========================
    try:

        cliente_socket.connect(
            (HOST, PORTA)
        )

    except ConnectionRefusedError:

        print(
            "[ERRO] Não foi possível conectar "
            "ao servidor."
        )

        print(
            f"[INFO] Verifique se o servidor "
            f"está rodando em {HOST}:{PORTA}"
        )

        return

    except Exception as erro:

        print(
            f"[ERRO] Falha na conexão: {erro}"
        )

        return

    print(
        f"[CONECTADO] Servidor "
        f"{HOST}:{PORTA}"
    )

    # ==========================
    # SOLICITAÇÃO DO NOME
    # ==========================

    resposta = cliente_socket.recv(
        1024
    ).decode("utf-8")

    if resposta == "SOLICITAR_NOME":

        nome = input(
            "Digite seu nome: "
        ).strip()

        if not nome:
            nome = "Anônimo"

        cliente_socket.send(
            nome.encode("utf-8")
        )

    # ==========================
    # INFORMAÇÕES INICIAIS
    # ==========================

    print(
        "\n================================"
    )

    print(
        "          CHAT INICIADO"
    )

    print(
        "================================"
    )

    print(
        "Pressione CTRL+C para sair."
    )

    print(
        "================================"
    )

    print(
        "\nIniciando chat..."
    )

    input(
        "Pressione ENTER para continuar..."
    )

    # ==========================
    # INICIA O CHAT
    # ==========================

    curses.wrapper(
        lambda tela: Chat(
            tela,
            cliente_socket
        ).executar()
    )

    print(
        "\n[INFO] Saindo do chat..."
    )


if __name__ == "__main__":
    iniciar_cliente()