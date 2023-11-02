import socket

# Establish a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the localhost IP address and a specific port number
serverIP = 'localhost'
serverPort = 1024
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