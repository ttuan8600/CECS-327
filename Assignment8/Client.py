import socket
import ipaddress
import threading
import time
import contextlib
import errno

maxPacketSize = 1024
defaultPort = 8000  # TODO: Change this to your expected port
serverIP = 'localhost'  # TODO: Change this to your instance IP

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tcpPort = int(input("Please enter the TCP port of the host..."))
except:
    tcpPort = 0
if tcpPort == 0:
    tcpPort = defaultPort
tcpSocket.connect((serverIP, tcpPort))

clientMessage = ""
while clientMessage != "exit":
    clientMessage = input("Type 'query for road' (Or type \"exit\" to exit):\n>")

    # TODO: Send the message to your server
    if clientMessage.startswith('query for road'):
        tcpSocket.send(clientMessage.encode())
        # TODO: Receive a reply from the server for the best highway to take
        serverReply = tcpSocket.recv(maxPacketSize).decode()
        # TODO: Print the best highway to take
        print(f"Best road to take: {serverReply}")
    else:
        print('invalid input!')

    print('\n')

tcpSocket.close()
