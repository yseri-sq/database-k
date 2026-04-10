from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db.db import get_session
from models.model import Hotel
from models.schemas import HotelAdd, HotelGet, HotelUpdate

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.post("/add", response_model=HotelGet, summary="Добавить новый отель/офис")
def add_location(location: HotelAdd, db: Session = Depends(get_session)):
    location_db = Hotel.model_validate(location)
    db.add(location_db)
    db.commit()
    db.refresh(location_db)
    return location_db

@router.get("/", response_model=List[HotelGet], summary="Получить список всех отелей")
def get_all_hotel(db: Session = Depends(get_session)):
    locations = db.exec(select(Hotel)).all()
    return locations

@router.put("/update/{loc_id}", response_model=HotelGet, summary="Обновить информацию")
def update_hotel(loc_id: int, loc: HotelUpdate, db: Session = Depends(get_session)):
    loc_db = db.get(Hotel, loc_id)
    if not loc_db:
        raise HTTPException(status_code=404, detail="Офис не найден")
    
    # Обновляем только те поля, которые переданы (exclude_unset=True)
    loc_data = loc.model_dump(exclude_unset=True)
    for key, value in loc_data.items():
        setattr(loc_db, key, value)
        
    db.add(loc_db)
    db.commit()
    db.refresh(loc_db)
    return loc_db

@router.delete("/delete/{loc_id}", summary="Удалить информацию")
def delete_hotel(loc_id: int, db: Session = Depends(get_session)):
    loc_db = db.get(Hotel, loc_id)
    if not loc_db:
        raise HTTPException(status_code=404, detail="Офис не найден")
    
    db.delete(loc_db)
    db.commit()
    return {"ok": True, "message": f"Отель <{loc_db.name}> успешно удален"}