from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import date

from db.db import get_session
from models.model import User
from models.schemas import UserReg, UserGet, UserUpdate, UserLog
from security.security import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["Users"])
current_user = None

@router.post("/reg", summary="Регистрация")
def reg(user : UserReg, db : Session = Depends(get_session)):
    user_db = User(**user.model_dump())
    user_db.hash_password = hash_password(user_db.hash_password)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return f"Пользователь <{user_db.FIO}> успешно зарегистрирован"

@router.post("/auth")
def auth(user: UserLog, db: Session = Depends(get_session)):
    user_db = db.exec(select(User).where(User.email == user.email)).first()
    
    if not user_db or not verify_password(user.hash_password, user_db.hash_password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    # Логика с админом (лучше хранить роль в БД изначально)
    if user_db.email == "admin@example.com":
        # Убедись, что в модели User есть поле role
        user_db.role = "admin" 
    
        db.add(user_db)
        db.commit()
        global current_user
        current_user = user_db
    return {"message": f"Добро пожаловать, {user_db.FIO}", "user_id": user_db.id}

@router.get("/", response_model=List[UserGet], summary="Получить список всех пользователей")
def get_all_users(db : Session = Depends(get_session)):
    users = db.exec(select(User)).all()
    return users

@router.put("/update/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_session)):
    user_db = db.get(User, user_id)
    if current_user.role != "admin":
        raise HTTPException(403, "Нет прав доступа")
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    
    # Исправлено: обращение к FIO вместо name
    user_db.email = user.email if user.email else user_db.email
    user_db.phone = user.phone if user.phone else user_db.phone
    
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return f"Данные пользователя <{user_db.FIO}> обновлены"
@router.delete("/delete/{user_id}", summary="Удалить пользователя")
def delete_user(user_id : int, db : Session = Depends(get_session)):
    user_db = db.exec(select(User).where(User.id == user_id)).first()
    if current_user.role != "admin":
        raise HTTPException(403, "Нет прав доступа")
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    
    db.delete(user_db)
    db.commit()

    return f"Пользователь успешно удален"