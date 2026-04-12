import uvicorn
from fastapi import FastAPI

from db.db import create_db_and_tables
from routers import users, categories, rooms,hotels

app = FastAPI()

app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(hotels.router)
# app.include_router(categories.router)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("main:app", reload=True)