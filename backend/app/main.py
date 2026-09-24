# Creates and configures the FastAPI application and 
# defines the API entry points.
from fastapi import FastAPI

app = FastAPI(  ##an instance of the FastAPI class is created, which represents the web application.
    title="Haver API",
    version="0.1.0",
)

## when a GET request is made to the "/health" endpoint, the health_check function is called, which returns a JSON response indicating that the application is running and healthy.
@app.get("/health")
def health_check():
    return {"status": "ok"}