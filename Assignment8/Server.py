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
defaultPort = 9990  # TODO: Set this to your preferred port


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
        query = tcpSocket.recv(maxPacketSize).decode()
        print(query)
        if query.startswith('traffic'):
            query = query.strip()
            sensor = query[query.index('<') + 1 : query.index('>')]
            print(sensor)
            mongoData = GetServerData(sensor)
            if mongoData is None:
                tcpSocket.send("invalid sensor".encode())
            else:
                mongoData = mongoData[1]
                total = 0
                length = mongoData[0].length
                for doc in mongoData:
                    total += doc.value
                tcpSocket.send(f"total:{total}, len:{length}".encode())

        if query.startswith('best road'):
            roadA = CalculateBestHighway('Traffic Data A')
            roadB = CalculateBestHighway('Traffic Data B')
            roadC = CalculateBestHighway('Traffic Data C')
            result = roadA
            if roadB[1] < result[1]:
                result = roadB

            if roadC[1] < result[1]:
                result = roadC
            tcpSocket.send(result[0].strip().split('/')[1].encode())

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
