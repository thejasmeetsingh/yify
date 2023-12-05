"""
Main App
"""

import os
from fastapi import FastAPI
from dotenv import load_dotenv

from peewee import PostgresqlDatabase

app = FastAPI()
load_dotenv()

# Testing DB connection
db = PostgresqlDatabase(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)


@app.get("/health-check/")
async def root():
    """
    Endpoint for checking if services are up or not
    """
    return {"message": "Up & Running!"}
