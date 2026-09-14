# pychat-socket
Simulação de um bate papo utilizando socket de rede

## Implementação do Chat

O projeto consiste em uma aplicação de chat desenvolvida em Python utilizando sockets TCP e comunicação concorrente por meio de threads. O sistema permite a conexão de até dois clientes simultaneamente, sendo cada usuário identificado por um nome informado durante o estabelecimento da conexão.

O `servidor.py` é responsável por estabelecer a conexão, gerenciar os clientes conectados e encaminhar as mensagens entre os usuários. Cada cliente possui uma thread responsável pelo recebimento das mensagens, permitindo que a comunicação ocorra de forma simultânea. As mensagens são encaminhadas aos demais clientes conectados, sem que o servidor envie novamente a mensagem ao próprio remetente.

O `cliente.py` utiliza a biblioteca `curses` para fornecer uma interface de terminal organizada, separando a área de exibição das mensagens da área destinada à digitação. As mensagens enviadas pelo próprio usuário são exibidas com a identificação `[Você]`, enquanto as mensagens recebidas apresentam o nome do remetente. O cliente também permite o envio das mensagens utilizando `Enter`, exclusão de caracteres com `Backspace` e encerramento da aplicação com `Ctrl+C`.

A comunicação utiliza o protocolo TCP, garantindo uma conexão orientada e confiável entre o cliente e o servidor. Dessa forma, o projeto demonstra a aplicação de conceitos de programação de redes, comunicação cliente-servidor, sockets e programação concorrente em Python.
