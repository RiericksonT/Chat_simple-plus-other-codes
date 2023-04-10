import socket

# Define the address and port of the message server
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 5000

# Define the address and port of the proxy server
PROXY_ADDRESS = 'localhost'
PROXY_PORT = 6000

# Create a socket for the proxy server
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.bind((PROXY_ADDRESS, PROXY_PORT))
proxy_socket.listen(1)
print(f'Proxy server listening on {PROXY_ADDRESS}:{PROXY_PORT}')

while True:
    # Wait for a client to connect to the proxy server
    client_socket, client_address = proxy_socket.accept()
    print(f'Client connected from {client_address}')

    # Connect to the message server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    # Forward messages between the client and the server
    while True:
        # Receive a message from the client
        message = client_socket.recv(1024)
        if not message:
            # The client has disconnected
            break
        # Forward the message to the server
        server_socket.sendall(message)

        # Receive a message from the server
        message = server_socket.recv(1024)
        if not message:
            # The server has disconnected
            break
        # Forward the message to the client
        client_socket.sendall(message)

    # Close the sockets
    client_socket.close()
    server_socket.close()
