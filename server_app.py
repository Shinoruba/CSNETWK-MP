import socket
import threading
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024
FILES_DIR = './server_files/'

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

class FileExchangeServer:
    def __init__(self):
        self.tcp_server = None
        self.clients = {}

    def start(self):
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.bind((SERVER_IP, SERVER_PORT))
        self.tcp_server.listen(5)
        print(f"TCP Server listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            client_socket, addr = self.tcp_server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

    def handle_client(self, client_socket, addr):
        print(f"Client connected: {addr}")
        handle = None
        while True:
            try:
                data = client_socket.recv(BUFFER_SIZE).decode()
                if not data:
                    break
                command, *args = data.split()
                if command == "REGISTER":
                    handle = args[0]
                    if handle in self.clients:
                        client_socket.send("Error: Registration failed. Handle or alias already exists.".encode())
                    else:
                        self.clients[handle] = (client_socket, addr)
                        client_socket.send(f"Welcome {handle}!".encode())
                elif command == "STORE":
                    filename = args[0]
                    client_socket.send("READY".encode())  # Acknowledge readiness to receive file
                    with open(FILES_DIR + filename, 'wb') as f:
                        while True:
                            file_data = client_socket.recv(BUFFER_SIZE)
                            if file_data.endswith(b"EOF"):  # Check for end of file transfer
                                f.write(file_data[:-3])  # Write all but the EOF marker
                                break
                            f.write(file_data)
                    client_socket.send(f"Uploaded {filename}".encode())
                elif command == "GET":
                    filename = args[0]
                    filepath = FILES_DIR + filename
                    if os.path.exists(filepath):
                        with open(filepath, 'rb') as f:
                            while True:
                                file_data = f.read(BUFFER_SIZE)
                                if not file_data:
                                    break
                                client_socket.send(file_data)
                    else:
                        client_socket.send(f"Error: File not found in the server.".encode())
                elif command == "DIR":
                    files = os.listdir(FILES_DIR)
                    client_socket.send("\n".join(files).encode())
                else:
                    client_socket.send("Error: Command not found.".encode())
            except Exception as e:
                print(f"Error handling client {addr}: {e}")
                break
        if handle:
            del self.clients[handle]
        client_socket.close()
        print(f"Client disconnected: {addr}")

if __name__ == "__main__":
    server = FileExchangeServer()
    server.start()