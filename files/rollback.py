import sys
import json
import base64
import time
from files.modules.promotePrimary import mongoPrimary 
from pymongo import MongoClient

out = base64.b64decode(sys.argv[1])
hosts=json.loads(out)
src=hosts['src']
toBePrimary = src[0]
primary=''

if __name__ == "__main__":
    mongoPrimary(primary, toBePrimary)
