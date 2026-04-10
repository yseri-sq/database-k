from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func

from db.db import get_session
from models.model import Room
from models.schemas import RoomAdd, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/add")
def add_rooms(room: RoomAdd, db: Session = Depends(get_session)):
    room_db = Room.model_validate(room) # Более правильный способ в SQLModel
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return f"Комната {room_db.number} создана"

@router.get("/get/all-rooms")
def get_all_rooms(db: Session = Depends(get_session)):
    return db.exec(select(Room)).all()

@router.get("/get/{room_id}")
def get_room_id(room_id : int, db : Session = Depends(get_session)):
    room_db = db.exec(select(Room).where(Room.id == room_id)).first()
    if not room_db:
        raise HTTPException(404, "Not found")
    return room_db


@router.put("/update/{room_id}")
def update_room(room_id: int, room: RoomUpdate, db: Session = Depends(get_session)):
    room_db = db.get(Room, room_id) # Короткий поиск по ID
    if not room_db:
        raise HTTPException(404, "Room not found")
    
    room_db.number = room.number # Убрана запятая!
    room_db.price = room.price

    db.add(room_db)
    db.commit()
    return "Data updated"

@router.delete("/delete/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_session)):
    room_db = db.get(Room, room_id)
    if not room_db:
        raise HTTPException(404, "Not found")
    
    # Сохраняем номер перед удалением, чтобы вернуть в ответе
    room_number = room_db.number 
    db.delete(room_db)
    db.commit()
    # db.refresh(room_db)  <-- ОШИБКА: нельзя рефрешить удаленный объект
    return f"Room {room_number} Deleted"