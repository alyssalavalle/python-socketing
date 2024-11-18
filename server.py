import socket
import threading

# Server setup
SERVER_HOST = '127.0.0.1'  # Localhost for testing; change if needed
SERVER_PORT = 12345
clients = {}  # Dictionary to store clients
usernames = {}  # Dictionary to map sockets to usernames

def broadcast(message, sender_socket=None):
    # Broadcasts a message to all clients except the sender.
    for client in clients.values():
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # Handle the case if sending fails (e.g., client disconnected)
                client.close()
                remove_client(client)

def handle_client(client_socket, address):
    # Handles communication with a connected client.
    try:
        # Prompt the client for a username
        client_socket.send("Please enter a username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        
        # Register client and announce their entry
        clients[username] = client_socket
        usernames[client_socket] = username
        print(f"[NEW CONNECTION] {username} connected from {address}.")
        broadcast(f"{username} has joined the chat!")

        # Listen for messages from the client
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            
            if message == "[DISCONNECT]":
                # Handle client-initiated disconnection
                print(f"[DISCONNECTION] {username} disconnected.")
                broadcast(f"[SERVER] {username} has left the chat!")
                client_socket.close()
                remove_client(client_socket)
                break
            
            elif message.startswith("/private"):
                # Private messaging command
                _, target_username, private_message = message.split(" ", 2)
                if target_username in clients:
                    clients[target_username].send(f"[PRIVATE] {username}: {private_message}".encode('utf-8'))
                else:
                    client_socket.send(f"[ERROR] User {target_username} not found.".encode('utf-8'))
            else:
                # Broadcast the regular message
                broadcast(f"{username}: {message}", client_socket)
    
    except (ConnectionResetError, ConnectionAbortedError):
        # Handle abrupt disconnections
        print(f"[DISCONNECTION] {usernames.get(client_socket, 'Unknown user')} disconnected unexpectedly.")
        broadcast(f"[SERVER] {usernames.get(client_socket, 'Unknown user')} has left the chat!")
        remove_client(client_socket)

def remove_client(client_socket):
    # Removes the client from the server's active list.
    username = usernames.get(client_socket)
    if username:
        del clients[username]
        del usernames[client_socket]

def start_server():
    # Starts the server and listens for incoming connections.
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