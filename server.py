import socket
import threading

# Set up server parameters
SERVER_HOST = '127.0.0.1'  # Localhost for testing; change if needed
SERVER_PORT = 12345
clients = []

# Function to broadcast messages to all connected clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Handle client disconnection
                clients.remove(client)

# Function to handle communication with a connected client
def handle_client(client_socket, address):
    print(f"{address} connected.")
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"[{address}] {message.decode('utf-8')}")
                broadcast(message, client_socket)
            else:
                raise Exception("Client disconnected")
        except:
            print(f"{address} disconnected.")
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen()
    print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        print(f"{threading.active_count()}")

if __name__ == "__main__":
    start_server()