import os
import pymongo
import datetime

uri = os.environ['MONGO_LOG']

mongo_client = pymongo.MongoClient(uri)
mongo_db = mongo_client["knidlog"]
mongo_col = mongo_db["logs"]
mongo_cou = mongo_db["users"]

def log_access(info):
    info["date"] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
    try:
        res = mongo_col.insert_one(info)
    except Exception as e:
        pass

def get_users():
    try:
        list_of_dict = list(mongo_cou.find({'email': {'$exists': 1}}))
        return [x['email'] for x in list_of_dict]
    except Exception as e:
        return []

def reg_user(data):
    try:
        res = mongo_cou.insert_one({'email': data})
    except Exception as e:
        pass

def get_field(field):
    try:
        retv = list(mongo_cou.find({field: {'$exists': 1}}))[0][field]
        return retv
    except Exception as e:
        return None
