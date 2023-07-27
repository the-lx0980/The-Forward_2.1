from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import Config

DATABASE_URI, DATABASE_NAME, COLLECTION_NAME = Config.DATABASE_URI, Config.DATABASE_NAME, Config.COLLECTION_NAME

client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

async def save_data(id, channel, message_id, caption, file_type):
    data = {
        '_id': id,
        'channel': channel,
        'file_type': file_type,
        'message_id': message_id,
        'use': 'forward',
        'caption': caption
    }
    
    try:
        collection.insert_one(data)
        print("Message saved in the database")
    except DuplicateKeyError:
        print("Already saved in the database")
    except Exception as e:
        print(f"Error occurred while saving file in the database: {e}")

async def get_search_results():
    filter = {'use': "forward"}
    messages = collection.find(filter).sort('$natural', -1).limit(1)
    return messages
