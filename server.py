from fastapi import FastAPI
from connection import databaseCRUD
from main import get_recommendations

app = FastAPI()

dbo = databaseCRUD.DatabaseObject()
dbo.connect()

@app.get("/")
def index_page(page_no: int = 1 ):
    data = dbo.displayData(page_no)
    count = dbo.countDocuments()
    return {"data":data, "count": count}

@app.get("/{food_name}")
def food_recommendation(food_name: str = None):
    recommended_food = []
    foods = get_recommendations(food_name)
    target_food = dbo.findFood(food_name)
    for food in foods:
        recommended_food.append(dbo.findFood(food[0]))
    return {"target_food": target_food, "recommended_food": recommended_food}