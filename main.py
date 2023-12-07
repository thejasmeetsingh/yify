"""
Main App
"""

from fastapi import FastAPI

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


@app.get("/health-check/")
async def health_check():
    """
    Endpoint for checking if services are up or not
    """
    return {"message": "Up & Running!"}
