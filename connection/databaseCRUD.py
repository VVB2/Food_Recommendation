import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps

load_dotenv()

class DatabaseObject:
    def __init__(self) -> None: 
        self.URI = os.environ['MONGO_URI']
        self.DATABASE = None   
        print("Connection established")

    def connect(self):
        try:
            self.client = MongoClient(self.URI)
            self.DATABASE = self.client['FoodDatabase']
        except Exception as e:
            print(e)
            self.disconnect()

    def disconnect(self):
        try:
            self.client.close()
        except Exception as e:
            print(e)

    def insertOne(self, data):
        self.DATABASE['Food'].insert_one(data)

    def displayData(self, pageNo):
        data = []
        no_of_data = 20
        cursor = list(self.DATABASE['Food'].find({}, {"_id": 0}).skip(no_of_data * pageNo).limit(no_of_data))
        for document in cursor:
            data.append(document)
        return data

    def __enter__(self):
        try:
            self.client = MongoClient(self.URI)
            self.DATABASE = self.client['FoodDatabase']
        except Exception as e:
            print(e)
            self.__exit__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.client.close()
        except Exception as e:
            print(e)