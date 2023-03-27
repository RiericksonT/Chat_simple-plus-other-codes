import socket
import threading

# Configurações do servidor
HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

# Lista de clientes conectados e canais criados
connections = []
clientes = []
canais = []
count_id = 0

#função de boas vindas
def welcome(client_socket, client_address):
    print(f'Novo cliente conectado: {client_address, client_socket}')
    client_socket.send("Bem-vindo ao Biscord! Este é um sistema de comunicação moderno que permite que você se conecte com amigos\n"
                        "colegas e clientes de maneira rápida e fácil. Aqui você pode compartilhar arquivos, criar salas de bate-papo\n"
                        "e muito mais. Esperamos que você tenha uma ótima experiência aqui!"
                        "Digite a opção que voce queira acessar:\n"
                        "1- Criar uma conta         2- fazer login".encode('utf-8'))
    
    opcao = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    if opcao == '1':
        cadastrar_cliente(client_socket, client_address)
    elif opcao == '2':
        login(client_socket, client_address)
    else:
        client_socket.send('Opção inválida'.encode('utf-8'))

#Função para cadastrar um novo canal de comuicação
def cadastrar_canal(client_socket, client_address):
    client_socket.send('Qual o nome do canal?'.encode('utf-8'))
    name = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    canais.append({
        'socket': client_socket,
        'address': client_address,
        'name': name,
        'id': count_id + 1
    })
    print(f'Novo canal criado: {client_address, name}')
    client_socket.send('Canal criado com sucesso'.encode('utf-8'))
    client_socket.send('Digite a opção que voce queira acessar:\n'
                                    '1- Entrar em um canal         2- Sair'.encode('utf-8'))
    opcao = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    if opcao == '1':
        entrar_canal(client_socket, client_address)
    if opcao == '2':
        client_socket.close()

# Função para cadastrar um novo cliente
def cadastrar_cliente(client_socket, client_address):
    client_socket.send('Qual seu nome?'.encode('utf-8'))
    name = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    client_socket.send('Qual sua senha?'.encode('utf-8'))
    password = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    try:
        clientes.append({
        'socket': client_socket,
        'address': client_address,
        'name': name,
        'password': password
    })
        client_socket.send('Cadastro realizado com sucesso'.encode('utf-8'))
    except:
        client_socket.send('Erro ao cadastrar'.encode('utf-8'))
    print(f'Novo cliente cadastrado: {client_address, name}')
    client_socket.send('Digite a opção que voce queira acessar:\n'
                                    '1- Fazer login         2- Sair'.encode('utf-8'))
    opcao = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    if opcao == '1':
        login(client_socket, client_address)
    if opcao == '2':
        client_socket.close()

#função de login
def login(client_socket, client_address):
    client_socket.send('Qual seu nome?'.encode('utf-8'))
    name = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    client_socket.send('Qual sua senha?'.encode('utf-8'))
    password = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    for c in clientes:
        if c['name'] == name and c['password'] == password:
            client_socket.send('Login realizado com sucesso'.encode('utf-8'))
            client_socket.send('Digite a opção que voce queira acessar:\n'
                                 '1- Criar um canal         2- Entrar em um canal'.encode('utf-8'))
            opcao = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if opcao == '1':
                cadastrar_canal(client_socket, client_address)
            if opcao == '2':
                entrar_canal(client_socket, client_address)
        else:
            continue
    client_socket.send('Login ou senha incorretos'.encode('utf-8'))    

# Função para lidar com um novo cliente
def handle_client(client_socket, client_address):
    name = ''
    while True:
        for client in clientes:
            if client['socket'] == client_socket:
                name = client['name']
        message = (f'{name}: ' + client_socket.recv(BUFFER_SIZE).decode('utf-8'))
        if not message:
            # O cliente desconectou
            clientes.remove(client_socket)
            print(f'Cliente desconectado: {client_address}')
            break
        
        elif message == 'sair do chat':
            # O cliente desconectou
            clientes.remove(client_socket)
            print(f'Cliente desconectado: {client_address}')
            break
        else:
            # Encaminha a mensagem para todos os outros clientes
            for c in clientes:
                if c['socket'] != client_socket:
                    c['socket'].send(message.encode('utf-8'))

#função pra o usuario entrar em um canal existentes
def entrar_canal(client_socket, client_address):
    client_socket.send('Qual o nome do canal?'.encode('utf-8'))
    name = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    for c in canais:
        if c['name'] == name:
            c['socket'].send(f'{client_socket} entrou no canal'.encode('utf-8'))
            handle_client(client_socket, client_address)


# Configura o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f'Servidor iniciado em {HOST}:{PORT}')

# Loop principal do servidor
while True:
    # Espera um novo cliente se conectar
    client_socket, client_address = server_socket.accept()
    connections.append(client_socket)

     # Cria uma nova thread para lidar com o cliente
    client_thread = threading.Thread(target=welcome, args=(client_socket, client_address))
    client_thread.start()
    print (f'Conexão de {client_address} estabelecida.')
    

    
