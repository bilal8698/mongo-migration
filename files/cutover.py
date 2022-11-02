import sys
import json
import base64
import socket
import time
from pymongo import MongoClient

out = base64.b64decode(sys.argv[1])
hosts=json.loads(out)
dest=hosts['dest']
toBePrimary = dest[0]

def cutover():
    client = MongoClient('0.0.0.0', 27017)
    db = client.admin
    helloOut = db.command("hello")
    primary = helloOut['primary'].split(":")[0]

    client = MongoClient(primary, 27017)
    db = client.admin
    replSetConfig=db.command("replSetGetConfig", 1)['config']
    members=replSetConfig['members']

    saddr=socket.gethostbyaddr(toBePrimary)

    for item in members:
        if saddr[0] in item['host'] or ''.join(saddr[2]) in item['host']:
            item['priority'] = 2
            break

    replSetConfig['members']=members
    replSetConfig['version'] += 1
    res = db.command('replSetReconfig', replSetConfig)
    
    time.sleep(180)

    helloOut = db.command("hello")
    primaryIP = helloOut['primary'].split(":")[0]

    client = MongoClient(primaryIP, 27017)
    db = client.admin
    replSetStatus=db.command('replSetGetStatus', 1)
    output={}
    for item in replSetStatus['members']:
        new={}
        new['health']=item['health']
        new['stateStr']=item['stateStr']
        new['uptime']=item['uptime']
        output[item['name']]=new
    print(output)

if __name__ == "__main__":
    cutover()

