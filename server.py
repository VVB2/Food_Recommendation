import math
import json
from flask import Flask, render_template, request
from connection import databaseCRUD
from main import get_recommendations

app = Flask(__name__)

dbo = databaseCRUD.DatabaseObject()
dbo.connect()

def get_page_range(page, total, show=10):
    start = max((page - (show // 2)), 1)
    stop = min(start + show, total) + 1
    start = max(min(start, stop - show), 1)
    return list(range(start, stop)[:show])

@app.route("/")
def index_page():
    page_no = int(request.args.get('page_no') or 1) 
    count = get_page_range(page_no, math.ceil(10179 / 20))
    data = dbo.displayData(page_no)
    return render_template('homePage.html', total_count=count, data=data, page_no=page_no)  

@app.route("/<string:food_name>")
def food_recommendation(food_name: str):
    recommended_food = []
    foods = get_recommendations(food_name)
    target_food = dbo.findFood(food_name)
    for food in foods:
        recommended_food.append(dbo.findRecommendedFood(food[0]))
    return render_template('foodRecommendationPage.html', target_food=target_food, recommended_food=recommended_food)

if __name__=="__main__":
    app.run(debug=True)