import socket

# Establish a TCP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ask user for server IP address and port number
serverIP = input("Enter server IP address: ")
serverPort = int(input("Enter server port number: "))

# Connect to the server
clientSocket.connect((serverIP, serverPort))

# Ask user for message to send to server
message = input("Enter a message to send to the server: ")

# Send the message to the server
clientSocket.send(bytearray(str(message), encoding='utf-8'))

# Receive data from server and print it
print("Message from server: " + str(clientSocket.recv(1024)))

# Close the socket
clientSocket.close()