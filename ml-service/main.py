from fastapi import FastAPI
from routes import ml

app = FastAPI()

app.include_router(ml.router)

@app.get("/")
def root():
    return {"message": "ML API running"}