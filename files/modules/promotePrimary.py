import sys
import json
import base64
import socket
import time
from pymongo import MongoClient

def mongoPrimary(primary, toBePrimary):
    '''
    Function to promote Mongo Cluster's Primary Node.
    Parameters:
        primary:        Current Primary Node of Mongo Cluster
        toBePrimary:    Node to be Promoted to Primary Node of Mongo Cluster       
    '''
    client = MongoClient('0.0.0.0', 27017)
    db = client.admin
    helloOut = db.command("hello")
    primary = helloOut['primary'].split(":")[0]
    addr=socket.gethostbyaddr(toBePrimary)

    client = MongoClient(primary, 27017)
    db = client.admin
    replSetConfig=db.command("replSetGetConfig", 1)['config']
    members=replSetConfig['members']

    for item in members:
        if addr[0] in item['host'] or ''.join(addr[2]) in item['host']:
            item['priority'] = priority(primary) + 1
            break

    replSetConfig['members']=members
    replSetConfig['version'] += 1
    res = db.command('replSetReconfig', replSetConfig)
    output=resetPriority(primary, toBePrimary)
    print(output)

def priority(primary):
    '''
    Function to return the Mongo Node Priority 
    Parameters:
        primary: Mongo node whose priority needs to be returned.
    '''
    client = MongoClient(primary, 27017)
    db = client.admin
    replSetConfig=db.command("replSetGetConfig", 1)['config']
    members=replSetConfig['members']
    for item in members:
        if primary in item['host']:
            return item['priority']

def resetPriority(primary, toBePrimary):
    '''
    Function to change priority of Mongo Node to promote.
    Parameters:
        primary:        Current Primary Node of Mongo Cluster
        toBePrimary:    Node to be Promoted to Primary Node of Mongo Cluster  
    '''
    time.sleep(180)
    output={}
    addr=socket.gethostbyaddr(toBePrimary)
    client = MongoClient(primary, 27017)
    db = client.admin
    helloOut = db.command("hello")
    primary = helloOut['primary'].split(":")[0]
    paddr=socket.gethostbyaddr(primary)
    if toBePrimary in paddr[0] or toBePrimary in ''.join(paddr[2]) :
        client = MongoClient(primary, 27017)
        db = client.admin
        replSetConfig=db.command("replSetGetConfig", 1)['config']
        members=replSetConfig['members']
        for item in members:
            if addr[0] in item['host'] or ''.join(addr[2]) in item['host']:
                item['priority'] = priority(primary) - 1
        replSetConfig['members']=members
        replSetConfig['version'] += 1
        res = db.command('replSetReconfig', replSetConfig)

        replSetStatus=db.command('replSetGetStatus', 1)
        for item in replSetStatus['members']:
            new={}
            new['health']=item['health']
            new['stateStr']=item['stateStr']
            new['uptime']=item['uptime']
            output[item['name']]=new
        return output
    else:
        resetPriority(primary, toBePrimary)
