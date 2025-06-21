from fastapi import FastAPI
from .routes import router
from .postgres_db import database

app = FastAPI(
    title="Mongo + Redis + PostgreSQL + RabbitMQ    API",
    version="1.0.0",
    docs_url="/apis",
    redoc_url=None,
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API is live. Visit /apis for documentation."}
