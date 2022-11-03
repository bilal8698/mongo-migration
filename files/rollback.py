from pprint import pp
import sys
import json
import base64
import socket
import time
from pymongo import MongoClient

out = base64.b64decode(sys.argv[1])
hosts=json.loads(out)
src=hosts['src']
toBePrimary = src[0]
saddr=socket.gethostbyaddr(toBePrimary)
primary=''

def rollback():
    global primary
    client = MongoClient('0.0.0.0', 27017)
    db = client.admin
    helloOut = db.command("hello")
    primary = helloOut['primary'].split(":")[0]

    client = MongoClient(primary, 27017)
    db = client.admin
    replSetConfig=db.command("replSetGetConfig", 1)['config']
    members=replSetConfig['members']

    for item in members:
        if saddr[0] in item['host'] or ''.join(saddr[2]) in item['host']:
            item['priority'] = priority() + 1
            break

    replSetConfig['members']=members
    replSetConfig['version'] += 1
    res = db.command('replSetReconfig', replSetConfig)
    output=resetPriority()
    print(output)


def priority():
    global primary
    client = MongoClient(primary, 27017)
    db = client.admin
    replSetConfig=db.command("replSetGetConfig", 1)['config']
    members=replSetConfig['members']
    for item in members:
        if primary in item['host']:
            return item['priority']

def resetPriority():
    global primary
    time.sleep(180)
    output={}
    client = MongoClient(primary, 27017)
    db = client.admin
    helloOut = db.command("hello")
    if toBePrimary ==  helloOut['primary'].split(":")[0]:
        primary = helloOut['primary'].split(":")[0]
        client = MongoClient(primary, 27017)
        db = client.admin
        replSetConfig=db.command("replSetGetConfig", 1)['config']
        members=replSetConfig['members']
        for item in members:
            new={}
            if saddr[0] in item['host'] or ''.join(saddr[2]) in item['host']:
                item['priority'] = priority() - 1
            new['health']=item['health']
            new['stateStr']=item['stateStr']
            new['uptime']=item['uptime']
            output[item['name']]=new
        replSetConfig['members']=members
        replSetConfig['version'] += 1
        res = db.command('replSetReconfig', replSetConfig)
        return output
    else:
        resetPriority()

    

if __name__ == "__main__":
    rollback()

