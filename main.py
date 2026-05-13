from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import engine, Base

# Import tables agar create_all membaca semua table
import tables.users
import tables.dictionary
import tables.quiz

# Import routes
import routes.users as user_routes
from routes import dictionary
from routes import predict
from routes import ml
from routes import websocket
from routes import quiz
from routes import profile


app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files untuk upload gambar dictionary
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is running"}


# Routes
app.include_router(user_routes.router)
app.include_router(profile.router)
app.include_router(dictionary.router)
app.include_router(predict.router)
app.include_router(ml.router)
app.include_router(websocket.router)
app.include_router(quiz.router)