import json
from fastapi import FastAPI
from connection import databaseCRUD

app = FastAPI()

dbo = databaseCRUD.DatabaseObject()
dbo.connect()

@app.get("/")
def read_root():
    # with databaseCRUD.DatabaseObject() as dbo:
    data = dbo.displayData(3)
    return {"data":data}