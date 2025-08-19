from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers.auth.router import auth_router
version = "v1.0"

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Intializing API server...")
    ## This function allows the fastapi server to initiate the resouces which server is going to use
    ## Like initiating the database here
    yield
    
    # Here add the resources, script which server needs to perform before exiting the server.
    print("Exiting the API server...")
    
app = FastAPI(
    title= "PyEveryday",
    description= "Pyeveryday API for handeling the backend.",
    version=version,
    lifespan= life_span
)


### Add midelware here...

app.include_router(auth_router.router, prefix=f"/api/{version}/auth", tags=['auth'])