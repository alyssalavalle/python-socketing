import socket
import threading

# Set up server connection parameters
SERVER_HOST = '127.0.0.1'  # Localhost for testing; change if needed
SERVER_PORT = 12345

# Function to handle receiving messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{message} \n")
            else:
                print("Server Disconnected")
                break
        except:
            print("ERROR! Connection lost.")
            client_socket.close()
            break

# Function to send messages to the server
def send_messages(client_socket):
    while True:
        message = input()
        if message.lower() == "quit":
            print("Disconnecting...")
            print("Fully Disconnected.")
            client_socket.close()
            break
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

    # Start threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    start_client()