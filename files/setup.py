import sys
import json
import base64
import time
from pymongo import MongoClient

out = base64.b64decode(sys.argv[1])
hosts=json.loads(out)
dest=hosts['dest']

def addSecondary():
    client = MongoClient('0.0.0.0', 27017)
    db = client.admin
    helloOut = db.command("hello")
    primaryIP = helloOut['primary'].split(":")[0]

    client = MongoClient(primaryIP, 27017)
    db = client.admin
    replSetConfig=db.command("replSetGetConfig", 1)['config']
    members=replSetConfig['members']

    for item in dest:
        new={}
        new['_id'] = members[-1]['_id']+1
        new['host'] = item
        new['hidden'] = False
        new['priority'] = 0
        members.append(new)
        replSetConfig['members']=members
        replSetConfig['version'] += 1
        res = db.command('replSetReconfig', replSetConfig)

    time.sleep(300)
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
    addSecondary()

