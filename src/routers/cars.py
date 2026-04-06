from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db.db import get_session
from models.model import Car
from models.schemas import CarAdd, CarGet, CarUpdate

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.post("/add", summary="Добавить новую машину")
def add_car(car : CarAdd ,db : Session = Depends(get_session)):
    car_db = Car(**car.model_dump())
    db.add(car_db)
    db.commit()
    db.refresh(car_db)

    return f"Машина '{car_db.brand} {car_db.model}' была успешно добавлена"

@router.get("/get_all_available", response_model=List[CarGet], summary="Получить список всех доступных для аренды машин")
def get_all_available_cars(db : Session = Depends(get_session)):
    car_db = db.exec(select(Car).where(Car.available == True)).all()
    return car_db

@router.get("/get/{car_id}", response_model=CarGet, summary="Получить машину по id")
def get_car_by_id(car_id : int, db : Session = Depends(get_session)):
    car_db = db.exec(select(Car).where(Car.id == car_id)).first()
    return car_db

@router.put("/update/{car_id}", summary="Обновить информацию о машине")
def update_car(car_id : int, car : CarUpdate, db : Session = Depends(get_session)):
    car_db = db.exec(select(Car).where(Car.id == car_id)).first()

    car_db.available = car.avillible
    car_db.number = car.number
    db.commit()
    db.refresh(car_db)

    return f"Информация о машине: '{car_db.brand} {car_db.model}' была обновлена"

@router.delete("/delete/{car_id}", summary="Удалить информацию о машине")
def delete_car(car_id : int, db : Session = Depends(get_session)):
    car_db = db.exec(select(Car).where(Car.id == car_id)).first()
    db.delete(car_db)
    db.commit()
    db.refresh(car_db)

    return f"Машина '{car_db.brand} {car_db.model}' была успешно удалена"
