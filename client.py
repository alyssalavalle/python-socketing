import socket
import threading

SERVER_HOST = '127.0.0.1'  # Localhost for testing; change if needed
SERVER_PORT = 12345

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}")
            else:
                print("[SERVER DISCONNECTED]")
                break
        except:
            print("[ERROR] Connection lost.")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input()
        if message.lower() == "quit":
            client_socket.send("[DISCONNECT]".encode('utf-8'))
            print("[DISCONNECTING] Goodbye!")
            client_socket.close()
            break
        elif message.startswith("/private"):
            # Private message command
            client_socket.send(message.encode('utf-8'))
        elif message.strip():
            client_socket.send(message.encode('utf-8'))

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[CONNECTED] Connected to the server.")
    except Exception as e:
        print(f"[ERROR] Could not connect to the server: {e}")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    start_client()