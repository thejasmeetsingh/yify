from fastapi import APIRouter

router = APIRouter()

@router.get("/health-check/")
async def health_check():
    """
    Endpoint for checking if services are up or not
    """
    return {"message": "Up & Running!"}