import socket
import threading

# Server setup
SERVER_HOST = '127.0.0.1'  # Localhost for testing; change if needed
SERVER_PORT = 12345
clients = {}
usernames = {}

def broadcast(message, sender_socket=None):
    for client in clients.values():
        if client != sender_socket:
            client.send(message.encode('utf-8'))

def handle_client(client_socket, address):
    # User authentication (username input)
    client_socket.send("Please enter a username: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8').strip()
    clients[username] = client_socket
    usernames[client_socket] = username
    print(f"[NEW CONNECTION] {username} connected from {address}.")
    broadcast(f"[SERVER] {username} has joined the chat!")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("/private"):
                # Private message handling
                _, target_username, private_message = message.split(" ", 2)
                if target_username in clients:
                    clients[target_username].send(f"[PRIVATE] {username}: {private_message}".encode('utf-8'))
                else:
                    client_socket.send(f"[ERROR] User {target_username} not found.".encode('utf-8'))
            elif message:
                broadcast(f"{username}: {message}", client_socket)
        except:
            print(f"[DISCONNECTION] {username} disconnected.")
            broadcast(f"[SERVER] {username} has left the chat!")
            client_socket.close()
            del clients[username]
            del usernames[client_socket]
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()