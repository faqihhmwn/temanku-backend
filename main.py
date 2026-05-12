from routes import profile
from fastapi import FastAPI
from routes import ml
import routes.users as user_routes
from routes import predict
import tables.dictionary
from routes import dictionary
from config import engine, Base
from fastapi.staticfiles import StaticFiles
from routes import websocket
from routes import quiz


app = FastAPI()

# quiz
app.include_router(quiz.router)

#websocket
app.include_router(websocket.router)

# dictionary
app.include_router(dictionary.router)

# prediction
app.include_router(predict.router)

# AI
app.include_router(ml.router)

@app.get("/")
def root():
    return {"message": "API is running"}

import tables.quiz

app.include_router(user_routes.router)

Base.metadata.create_all(bind=engine)

# dictionary
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(dictionary.router)

# model predict
app.include_router(predict.router)

# users
app.include_router(user_routes.router)

# profile
app.include_router(profile.router)