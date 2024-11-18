import socket
import threading

SERVER_HOST = '127.0.0.1'  # Localhost for testing; change if needed
SERVER_PORT = 12345

def receive_messages(client_socket):
    # Receives messages from the server and displays them.
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{message}\n")
            else:
                print("[SERVER DISCONNECTED]")
                break
        except:
            print("Connection lost.")
            client_socket.close()
            break

def send_messages(client_socket):
    # Sends messages to the server from the user.
    print("Reminder: Type 'SEND' before each message to send it to the server.")
    
    while True:
        message = input()
        if message.lower() == "quit":
            client_socket.send("[DISCONNECT]".encode('utf-8'))
            print("[DISCONNECTING] Disconnected")
            client_socket.close()
            break
        elif message.startswith("/private"):
            client_socket.send(message.encode('utf-8'))
        elif message.startswith("SEND "):
            # Send only if message starts with "SEND"
            client_socket.send(message[5:].encode('utf-8'))  # Remove "SEND " prefix before sending
        else:
            print("Warning: 'SEND' must appear before every message or command to send it to the server.")

def start_client():
    # Starts the client and connects to the server.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        command = input("Type 'CONNECT' to connect to the server: ").strip()
        if command.upper() == "CONNECT":
            break
        else:
            print("Invalid command. Please type 'CONNECT' to connect.")

    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[CONNECTED] Connected to the server.")
    except Exception as e:
        print(f"[ERROR] Could not connect to the server: {e}")
        return

    # Start threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    start_client()