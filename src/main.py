import uvicorn
from fastapi import FastAPI, HTTPException

from db.db import create_db_and_tables
from routers import users, cars, locations

app = FastAPI()

app.include_router(users.router)
app.include_router(cars.router)
app.include_router(locations.router)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("main:app", reload=True)