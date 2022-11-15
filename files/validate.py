import sys
import json
from pymongo import MongoClient

def status():
    client = MongoClient('0.0.0.0', 27017)
    db = client.admin
    helloOut = db.command("hello")
    primaryIP = helloOut['primary'].split(":")[0]

    client = MongoClient(primaryIP, 27017)
    db = client.admin
    replSetStatus=db.command('replSetGetStatus', 1)
    output={}
    for item in replSetStatus['members']:
        new={}
        if item['health'] == 0:
            new['health']="DOWN"
        else:
            new['health']="UP"
        new['stateStr']=item['stateStr']
        new['uptime']=item['uptime']
        if item['lastHeartbeatMessage'] != "":
            new['lastHeartbeatMessage'] = item['lastHeartbeatMessage']
        output[item['name']]=new
    print(output)

if __name__ == "__main__":
    status()

