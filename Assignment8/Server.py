import socket
import ipaddress
import threading
import time
import contextlib
import errno
from collections import defaultdict
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


def GetServerData() -> []:
    return mongo.QueryDatabase()


def CalculateBestRoad(timedata) -> []:
    # TODO: Implement logic to calculate the best highway based on sensor data
    if not timedata:
        return "No data available"

        # Assuming timedata is a list of dictionaries with 'highway' and 'timestamp' keys
        # Example: [{'highway': 'A', 'timestamp': '2023-12-06T22:44:02.000+00:00'}, ...]

    road_times = defaultdict(list)

    # Group data by highway and collect timestamps
    for entry in timedata:
        road_times[entry['highway']].append(entry['timestamp'])

    # Calculate average time for each road
    avg_times = {}
    for road, timestamps in road_times.items():
        # Convert timestamps to datetime objects for calculations
        datetime_timestamps = [datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f%z") for ts in timestamps]

        # Calculate the time differences between timestamps
        time_diffs = [(ts - datetime_timestamps[i - 1]).total_seconds() / 60 for i, ts in enumerate(datetime_timestamps) if i > 0]

        # Calculate average time for the road
        avg_time = sum(time_diffs) / len(time_diffs) if time_diffs else 0
        avg_times[road] = avg_time

    # Find the road with the lowest average time
    best_road = min(avg_times, key=avg_times.get)

    return best_road


def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    # TODO: Implement TCP Code, use GetServerData to query the database.
    clientMessage = tcpSocket.recv(maxPacketSize).decode()
    if clientMessage:
        serverData = GetServerData()
        bestRoad = CalculateBestRoad(serverData)
        tcpSocket.send(bestRoad.encode())

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
    exitSignal = False
    while not exitSignal:
        time.sleep(1)
    print("Ending program by exit signal...")
