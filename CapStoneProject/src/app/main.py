from fastapi import FastAPI
from app.db_and_models.session import create_db_and_tables, drop_tables

app = FastAPI()

@app.get("/")
def placeholder():
    return {"message": "placeholder"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.on_event("shutdown")
def on_shutdown():
    drop_tables()