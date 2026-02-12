from fastapi import FastAPI
from app.routes import documents
from app.database.connection import init_db


app = FastAPI(title="Multi Document RAG")


@app.on_event("startup")
def startup_event():
    init_db()
    print("Daabase initialized")


app.include_router(documents.router)


@app.get("/")
def root():
    return {"message": "App started successfully"}
