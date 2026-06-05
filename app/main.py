"""Main module for the OdooConnectorAPI FastAPI application."""
from fastapi import APIRouter
from app.controllers import router as api_router

# Create an instance of the FastAPI application
app = APIRouter()

# Include routers from controllers
app.include_router(api_router)
