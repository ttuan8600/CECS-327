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

    # Receive data from client
    data = str(clientSocket.recv(1024))

    # Convert the received data to capital letters, print to terminal and send it back to the client
    capitalData = data.upper()
    print("Message from client: " + capitalData)
    clientSocket.send(bytearray(str(capitalData), encoding='utf-8'))

    clientSocket.close()