import sys
import json
import base64
import time
from pymongo import MongoClient

def validate():
    dbsrc={}
    dbdest={}
    out = base64.b64decode(sys.argv[1])
    hosts=json.loads(out)
    dest=hosts['dest'][0]
    src=hosts['src'][0]

    clientsrc = MongoClient(src, 27017)
    clientdest = MongoClient(dest, 27017)

    for database in clientsrc.list_databases():
        if 'admin' not in database['name'] and 'config' not in database['name'] and 'local' not in database['name']:
            dbsrc[database['name']] = database
    
    for database in clientdest.list_databases():
        if 'admin' not in database['name'] and 'config' not in database['name'] and 'local' not in database['name']:
            dbdest[database['name']] = database
    
    if set(dbsrc.keys()) != set(dbdest.keys()):
        return "Mismatch between Databases in Source and Destination Nodes"

    for name in dbsrc.keys():
        dbsrc=clientsrc[name]
        dbdest=clientdest[name]
        ressrc=dbsrc.command( "dbHash" , 1 )
        resdest=dbdest.command( "dbHash" , 1 )
        if set(ressrc['collections'].keys()) != set(resdest['collections'].keys()):
            return "Mismatch between Collections for "+name+" Database in Source and Destination Nodes"
        for col in ressrc['collections']:
            if ressrc['collections'][col] != resdest['collections'][col]:
                return "Collection Hash Mismatch - "+col+" Collection, Database - "+name
        
    return "Data Validation Successful"

if __name__ == "__main__":
    validate()

