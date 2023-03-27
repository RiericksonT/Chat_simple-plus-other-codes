import socket
import threading

# Configurações do cliente
HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        # Recebe a mensagem do servidor
        message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        if not message:
            # O servidor desconectou
            print('Servidor desconectado.')
            break
        else:
            # Exibe a mensagem na tela
            print(message)

# Configura o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Cria uma nova thread para receber mensagens do servidor
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()
name = input('Digite a opção: ')
client_socket.send(name.encode('utf-8'))

# Loop principal do cliente
while True:
    # Lê uma mensagem do usuário
    message = input('> ')

    # Envia a mensagem para o servidor
    client_socket.send(message.encode('utf-8'))
