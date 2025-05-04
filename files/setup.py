import sys
import json
import base64
import time
from pymongo import MongoClient

def addSecondary():
    try:
        out = base64.b64decode(sys.argv[1])
        hosts = json.loads(out)
        dest = hosts['dest']
        
        client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=5000)
        db = client.admin
        helloOut = db.command("hello")
        primaryIP = helloOut['primary'].split(":")[0]

        client = MongoClient(primaryIP, 27017, serverSelectionTimeoutMS=5000)
        db = client.admin
        replSetConfig = db.command("replSetGetConfig", 1)['config']
        members = replSetConfig['members']

        for item in dest:
            new_member = {
                '_id': members[-1]['_id'] + 1,
                'host': item,
                'hidden': False,
                'priority': 0,
                'votes': 1
            }
            members.append(new_member)
            replSetConfig['members'] = members
            replSetConfig['version'] += 1
            db.command('replSetReconfig', replSetConfig)
            print(f"Added {item} to replica set")

        time.sleep(180)  # Wait for sync
        
        replSetStatus = db.command('replSetGetStatus', 1)
        output = {}
        for member in replSetStatus['members']:
            output[member['name']] = {
                'health': member['health'],
                'stateStr': member['stateStr'],
                'uptime': member['uptime']
            }
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    addSecondary()