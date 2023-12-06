"""
Main App
"""

from fastapi import FastAPI
from routers import root

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
    application.include_router(root.router)

    return application

app = get_application()
