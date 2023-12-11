"""
Main App
"""

from fastapi import FastAPI, status
from pydantic import BaseModel

import strings


def get_application() -> FastAPI:
    """
    Initialize main app with nessecary configuration
    """

    application = FastAPI()

    # Add title and description of the application
    application.title = strings.APP_TITLE
    application.description = strings.APP_DESCRIPTION

    # Add routes of different apps
    # application.include_router(health_check.router)

    return application


app = get_application()


class HealthCheck(BaseModel):
    """
    Health check endpoint response schema
    """

    message: str


@app.get("/health-check/", status_code=status.HTTP_200_OK, response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """
    Endpoint for checking if services are up or not
    """

    return HealthCheck(message="Up & Running!")
