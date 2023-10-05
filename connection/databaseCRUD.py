import os
from dotenv import load_dotenv
from pymongo import MongoClient

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

    # def getFoodTitles(self):
    #     food_titles = []
    #     cursor = list(self.DATABASE['Food'].find({}, {"_id": 0, "ingredients": 0, "directions": 0, "link": 0, "narration": 0, "image_url": 0 }))
    #     for document in cursor:
    #         food_titles.append(document)
    #     return food_titles
    
    def findRecommendedFood(self, food):
        food_data = []
        cursor = list(self.DATABASE['Food'].find({'title': food}, {"_id": 0, "ingredients": 0, "directions": 0, "link": 0, "narration": 0}))
        for document in cursor:
            food_data.append(document)
        return food_data
        
    def findFood(self, food):
        food_data = []
        cursor = list(self.DATABASE['Food'].find({'title': food}, {"_id": 0}))
        for document in cursor:
            food_data.append(document)
        return food_data

    def displayData(self, pageNo):
        data = []
        no_of_data = 20
        cursor = list(self.DATABASE['Food'].find({}, {"_id": 0, "directions": 0, "link": 0, "narration": 0}).skip(no_of_data * pageNo).limit(no_of_data))
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