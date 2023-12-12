from pymongo import MongoClient, database
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta
import time

DBName = "test"  # Use this to change which Database we're accessing
connectionURL = "mongodb+srv://ttuan8600:qBmdFkQLeENoh4dH@cecs-326-029136612-twan.wbabn0a.mongodb.net/?retryWrites=true&w=majority"  # Put your database URL here
sensorTable = "Traffic Data ABC"  # Change this to the name of your sensor data table

def QueryToList(query):
    # TODO: Convert the query that you get in this function to a list and return it
    # HINT: MongoDB queries are iterable
    return list(query)


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
        # Update current documents
        if (len(currentDocuments)) == 0:
            currentDocuments = oldDocuments

        sensorA, sensorB, sensorC = 0, 0, 0
        for doc in currentDocuments:
            payload = doc['payload']
            if payload.get('Sensor A') != None:
                sensorA += payload.get('Sensor A')
            elif payload.get('Sensor B') != None:
                sensorB += payload.get('Sensor B')
            else:
                sensorC += payload.get('Sensor C')

        avgA, avgB, avgC = sensorA/5, sensorB/5, sensorC/5
        sensorData = [{"Freeway A": avgA, "Freeway B": avgB, "Freeway C": avgC}]
        print(sensorData)
        # Return that sensor data as a list
        return sensorData

    except Exception as e:
        print("Please make sure that this machine's IP has access to MongoDB.")
        print("Error:", e)
        exit(0)
