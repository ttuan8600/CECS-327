from pymongo import MongoClient, database
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta
import time

DBName = "test"  # Use this to change which Database we're accessing
connectionURL = "mongodb+srv://ttuan8600:qBmdFkQLeENoh4dH@cecs-326-029136612-twan.wbabn0a.mongodb.net/?retryWrites=true&w=majority"  # Put your database URL here
# sensorTable = "Traffic Data B"  # Change this to the name of your sensor data table


class SensorData:
    def __init__(self, length, topic, timestamp, device_asset_uid, sensor, value):
        self.length = length
        self.topic = topic
        self.timestamp = timestamp
        self.device_asset_uid = device_asset_uid
        self.sensor = sensor
        self.value = value

    def __str__(self):
        return 'length={} topic={} sensor={} value={}'.format(self.length, self.topic, self.sensor, self.value)


def QueryToList(query):
    # TODO: Convert the query that you get in this function to a list and return it
    # HINT: MongoDB queries are iterable
    data = []
    for doc in query:
        length = doc['length']
        topic = doc['topic']
        timestamp = doc['payload']['timestamp']
        device_asset_uid = doc['payload']['device_asset_uid']

        sensor = None
        value = None

        payload = doc['payload']
        for e in payload.keys():
            if e not in ('timestamp', 'topic', 'device_asset_uid'):
                sensor = e
                value = payload[e]

        data.append(
            SensorData(
                length,
                topic,
                timestamp,
                device_asset_uid,
                sensor,
                value
            )
        )
        return data


def QueryDatabase(sensorTable) -> []:
    global DBName
    global connectionURL
    global currentDBName
    global running
    global filterTime
    # global sensorTable
    cluster = None
    client = None
    db = None
    try:
        cluster = connectionURL
        client = MongoClient(cluster)
        db = client[DBName]
        print("Database collections: ", db.list_collection_names())

        # We first ask the user which collection they'd like to draw from.
        sensorTable = db[sensorTable]
        print("Table:", sensorTable)
        # We convert the cursor that mongo gives us to a list for easier iteration.
        timeCutOff = datetime.now() - timedelta(minutes=5)  # TODO: Set how many minutes you allow

        oldDocuments = QueryToList(sensorTable.find({"time": {"$gte": timeCutOff}}))
        currentDocuments = QueryToList(sensorTable.find({"time": {"$lte": timeCutOff}}))

        print("Current Docs:", currentDocuments)
        print("Old Docs:", oldDocuments)

        # TODO: Parse the documents that you get back for the sensor data that you need

        # Return that sensor data as a list
        return [oldDocuments, currentDocuments]

    except Exception as e:
        print("Please make sure that this machine's IP has access to MongoDB.")
        print("Error:", e)
        exit(0)
