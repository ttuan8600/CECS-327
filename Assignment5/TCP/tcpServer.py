import socket
import sys

if len(sys.argv) != 3:
    print("Usage: python server.py <server_ip> <server_port>")
    sys.exit(1)

# Get the server address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Establish a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the localhost IP address and a specific port number
serverSocket.bind((serverIP, serverPort))

# Start listening for incoming connections
serverSocket.listen(5)

while True:
    # Accept an incoming connection from a client
    clientSocket, clientAddress = serverSocket.accept()
    while True:
        # Receive data from client
        data = str(clientSocket.recv(1024))
        
        # close if client cut off connection
        if not data:
            break
        # print to terminal
        print("Message from client: " + data)
        # Convert the received data to capital letters and send it back to the client
        capitalized_Data = data.upper()
        clientSocket.send(bytearray(str(capitalized_Data), encoding='utf-8'))

    clientSocket.close()