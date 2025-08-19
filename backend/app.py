from fastapi import FastAPI

app = FastAPI()

@app.get("/check")
async def check():
    return {"message": "We are checking the API"}