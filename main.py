"""
Main App
"""

from fastapi import FastAPI
app = FastAPI()

@app.get("/health-check/")
async def root():
    """
    Endpoint for checking if services are up or not
    """
    return {"message": "Up & Running!"}
