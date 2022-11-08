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
    output={}

    for database in clientsrc.list_databases():
            dbsrc[database['name']] = database
    
    for database in clientdest.list_databases():
            dbdest[database['name']] = database
    
    if set(dbsrc.keys()) != set(dbdest.keys()):
        print("Mismatch between Databases in Source and Destination Nodes - Data Validation FAILED")
        return

    for name in dbsrc.keys():
        dbsrc=clientsrc[name]
        dbdest=clientdest[name]
        ressrc=dbsrc.command( "dbHash" , 1 )
        resdest=dbdest.command( "dbHash" , 1 )
        if ressrc['md5'] != resdest['md5']:
            print("Database "+name+" md5 hash does not match for Source "+src+" and Destination "+dest+" Mongo Node - Data Validation FAILED")
            return
        else:
            output[name]={'Source':ressrc['md5'] , 'Destination':resdest['md5']}
        
    print(output)


if __name__ == "__main__":
    validate()

