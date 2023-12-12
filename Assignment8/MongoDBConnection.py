from pymongo import MongoClient, database
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta
import time

DBName = "test"  # Use this to change which Database we're accessing
connectionURL = "mongodb+srv://ttuan8600:qBmdFkQLeENoh4dH@cecs-326-029136612-twan.wbabn0a.mongodb.net/?retryWrites=true&w=majority"  # Put your database URL here
sensorTable = "Traffic Data B"  # Change this to the name of your sensor data table

def QueryToList(query):
    # TODO: Convert the query that you get in this function to a list and return it
    # HINT: MongoDB queries are iterable
    parsed_data = []

    for entry in query:
        payload = entry.get('payload', {})
        road_sensor = payload.get('Road B Sensor')
        timestamp = payload.get('time')

        # Ensure both fields are available before appending to the list
        if road_sensor is not None and timestamp is not None:
            parsed_data.append({'highway': road_sensor, 'timestamp': timestamp})

    print(parsed_data)
    return parsed_data



def QueryDatabase() -> []:
    global DBName
    global connectionURL
    global currentDBName
    global running
    global filterTime
    global sensorTable
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
        timedata = []
        for entry in oldDocuments+currentDocuments:
            roadSensor = entry.get('topic')
            timestamp = entry.get('time')

            timedata.append({'highway': roadSensor, 'timestamp': timestamp})
        # Return that sensor data as a list
        return timedata

    except Exception as e:
        print("Please make sure that this machine's IP has access to MongoDB.")
        print("Error:", e)
        exit(0)
