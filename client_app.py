import socket
import os
from datetime import datetime

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024


#   CSNETWK S15 - Machine Project
#   
#   MP Finals Group 13:
#   CHAN, RIZZA MIKAELLA CHUA
#   HOMSSI, YAZAN MANAIG
#   VILLAMOR, GRANT SPENCER LIM

class FileExchangeClient:
    def __init__(self):
        self.tcp_socket = None
        self.handle = None

    def connect(self, ip, port):
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect((ip, port))
            print("Connection to the File Exchange Server is successful!")
        except:
            print("Error: Connection to the Server has failed! Please check IP Address and Port Number.")

    def disconnect(self):
        if self.tcp_socket:
            self.tcp_socket.close()
            self.tcp_socket = None
            self.handle = None
            print("Connection closed. Thank you!")
        else:
            print("Error: Not connected to any server.")

    def register(self, handle):
        if not self.tcp_socket:
            print("Error: Please connect to the server first.")
            return
        self.tcp_socket.send(f"REGISTER {handle}".encode())
        response = self.tcp_socket.recv(BUFFER_SIZE).decode()
        print(response)
        if response.startswith("Welcome"):
            self.handle = handle

    def store_file(self, filename):
        if not self.tcp_socket:
            print("Error: Please connect to the server first.")
            return
        if not os.path.exists(filename):
            print("Error: File not found.")
            return
        with open(filename, 'rb') as f:
            file_data = f.read()
        self.tcp_socket.send(f"STORE {filename}".encode())
        ack = self.tcp_socket.recv(BUFFER_SIZE).decode()
        if ack == "READY":
            self.tcp_socket.sendall(file_data)
            self.tcp_socket.send(b"EOF")  # Signal end of file transfer
            response = self.tcp_socket.recv(BUFFER_SIZE).decode()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{self.handle}<{timestamp}>: {response}")
        else:
            print("Error: Failed to store the file on the server.")

    def get_file(self, filename):
        if not self.tcp_socket:
            print("Error: Please connect to the server first.")
            return
        self.tcp_socket.send(f"GET {filename}".encode())
        response = self.tcp_socket.recv(BUFFER_SIZE)
        if response.startswith(b"Error"):
            print(response.decode())
        else:
            with open(filename, 'wb') as f:
                f.write(response)
            print(f"File received from Server: {filename}")

    def list_directory(self):
        if not self.tcp_socket:
            print("Error: Please connect to the server first.")
            return
        self.tcp_socket.send("DIR".encode())
        response = self.tcp_socket.recv(BUFFER_SIZE).decode()
        print("Server Directory")
        print(response)

    def show_help(self):
        print("Available commands:")
        print("/join <server_ip_add> <port> - Connect to the server")
        print("/leave - Disconnect from the server")
        print("/register <handle> - Register a unique handle or alias")
        print("/store <filename> - Send file to server")
        print("/dir - Request directory file list from server")
        print("/get <filename> - Fetch a file from server")
        print("/? - Show this help message")

def main():
    client = FileExchangeClient()
    while True:
        command = input("Enter command: ")
        if command.startswith("/join"):
            parts = command.split()
            if len(parts) == 3:
                _, ip, port = parts
                client.connect(ip, int(port))
            else:
                print("Error: /join command requires server IP and port.")
        elif command == "/leave":
            client.disconnect()
        elif command.startswith("/register"):
            parts = command.split()
            if len(parts) == 2:
                _, handle = parts
                client.register(handle)
            else:
                print("Error: /register command requires a handle.")
        elif command.startswith("/store"):
            parts = command.split()
            if len(parts) == 2:
                _, filename = parts
                client.store_file(filename)
            else:
                print("Error: /store command requires a filename.")
        elif command == "/dir":
            client.list_directory()
        elif command.startswith("/get"):
            parts = command.split()
            if len(parts) == 2:
                _, filename = parts
                client.get_file(filename)
            else:
                print("Error: /get command requires a filename.")
        elif command == "/?":
            client.show_help()
        else:
            print("Error: Command not found.")

if __name__ == "__main__":
    main()