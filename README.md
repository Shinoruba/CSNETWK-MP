# File Exchange System
## NOTE: The applications use only built-in Python modules:
- `socket`: For network communication.
- `threading`: For handling multiple client connections in the server.
- `os`: For file and directory operations.
- `datetime`: For timestamp generation in the client.

## Project Overview

This File Exchange System is a client-server application that enables clients to store, share, and fetch files from a single server using TCP protocol. The system consists of a server application and a client application.

## Specifications

### Client Application

The client application serves as the user interface for the File Exchange System.

#### Supported Commands

1. `/join <server_ip_add> <port>`: Connect to the server application
2. `/leave`: Disconnect from the server application
3. `/register <handle>`: Register a unique handle or alias
4. `/store <filename>`: Send file to server
5. `/dir`: Request directory file list from server
6. `/get <filename>`: Fetch a file from server
7. `/?`: Request command help to output all input syntax commands for reference

#### Sample Output Messages

- Successful connection: "Connection to the File Exchange Server is successful!"
- Successful disconnection: "Connection closed. Thank you!"
- Successful registration: "Welcome User1!"
- Successful file upload: "User1<2023-11-06 16:48:05>: Uploaded Hello.txt"
- Directory listing:
  - Server Directory
    - Hello.txt
    - Goodbye.txt
- Successful file retrieval: "File received from Server: Hello.txt"

### Server Application

The server application functions as the service to which client applications connect, facilitating interaction among clients in the File Exchange Application.

## Implementation Details

- The system is implemented in Python.
- It uses TCP protocol for communication between client and server.
- The server can handle multiple client connections simultaneously.
- Files are stored in a designated server directory.

## How to Run

1. Start the server application: `python server_app.py`
2. Run the client application: `python client_app.py`
3. Use the supported commands in the client application to interact with the server.

## Note

This project was developed as part of the CSNETWK course at De La Salle University for the Term 3 AY2023-2024.