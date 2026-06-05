"""Main module for the OdooConnectorAPI FastAPI application."""
from fastapi import FastAPI
from app.controllers import router as api_router

# Create an instance of the FastAPI application
app = FastAPI(title="OdooConnectorAPI", version="0.1.0")

# Include routers from controllers
app.include_router(api_router)
