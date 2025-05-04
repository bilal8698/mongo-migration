from pymongo import MongoClient
import time

def mongoPrimary(current_primary, new_primary):
    try:
        if current_primary:
            client = MongoClient(current_primary, 27017, serverSelectionTimeoutMS=5000)
            db = client.admin
            db.command('replSetStepDown', 60)
            time.sleep(10)
        
        client = MongoClient(new_primary, 27017, serverSelectionTimeoutMS=5000)
        db = client.admin
        db.command('replSetFreeze', 0)
        print(f"Successfully promoted {new_primary} to primary")
    except Exception as e:
        print(f"Error during promotion: {str(e)}")
        raise