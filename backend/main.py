from fastapi import FastAPI
from api import router

# Main file for the FastAPI application. It initializes the FastAPI app and includes the API router.
app = FastAPI()
app.include_router(router)
