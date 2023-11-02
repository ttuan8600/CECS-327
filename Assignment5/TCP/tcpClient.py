import socket

# Establish a TCP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ask user for server IP address and port number
serverIP = input("Enter server IP address: ")
serverPort = int(input("Enter server port number: "))

try:
    # Connect to the server
    clientSocket.connect((serverIP, serverPort))
    while True:
        # Ask user for message to send to server
        message = input("Enter a message to send to the server (or type 'exit' to exit): ")

        if message.lower() == 'exit':
            break

        # Send the message to the server
        clientSocket.send(bytearray(message, encoding='utf-8'))

        # Receive data from server and print it
        serverResponse = clientSocket.recv(1024)
        print("Message from server: " + serverResponse.decode('utf-8'))
        
except ConnectionRefusedError:
    print("Error: Connection to the server failed. Please check the IP address and port number.")
except Exception as e:
    print("An error occurred:", str(e))
    
finally:
    clientSocket.close()