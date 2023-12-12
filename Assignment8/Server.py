import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
from datetime import datetime, timedelta
import sys
import MongoDBConnection as mongo

maxPacketSize = 1024
defaultPort = 9900  # TODO: Set this to your preferred port


def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
    for i in range(minPort, maxPort):
        print("Testing port", i)
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
            try:
                potentialPort.bind(('localhost', i))
                potentialPort.close()
                print("Server listening on port", i)
                return i
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print("Port", i, "already in use. Checking next...")
                else:
                    print("An exotic error occurred:", e)


def GetServerData(sensorTable) -> []:
    return mongo.QueryDatabase(sensorTable)


def CalculateBestHighway(sensorTable) -> []:
    # TODO: Implement logic to calculate the best highway based on sensor data
    limit = datetime.now() - timedelta(minutes=5)
    data = mongo.QueryDatabase(sensorTable)
    l = data[0] + data[1]
    total = 0

    for sensorData in l:
        if float(sensorData.timestamp) >= limit.timestamp():
            total += sensorData.value

        return (l[0].topic, total / l[0].length)


def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    # TODO: Implement TCP Code, use GetServerData to query the database.
    while True:
        # Receive data from the client
        receiveData = tcpSocket.recv(maxPacketSize).decode()
        query = recv_data.decode()
        # Get server data and calculate the best highway
        serverData = GetServerData()
        bestHighway = CalculateBestHighway(serverData)

        # Send the best highway back to the client
        tcpSocket.send(bestHighway.encode())


def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpPort = defaultPort
    print("TCP Port:", tcpPort)
    tcpSocket.bind(('localhost', tcpPort))
    return tcpSocket


def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket()
    tcpSocket.listen(5)
    while True:
        connectionSocket, connectionAddress = tcpSocket.accept()
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress])
        connectionThread.start()


if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads)
    tcpThread.start()
    exitSignal = 0
    while not exitSignal:
        time.sleep(1)
    print("Ending program by exit signal...")
