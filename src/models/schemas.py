from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserReg(BaseModel):
    FIO: str
    email: EmailStr
    phone: str
    passport: str
    date_birth: date

class UserGet(BaseModel):
    id: int
    FIO: str
    email: EmailStr

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class RoomAdd(BaseModel):
    number: str
    hotel_id: int
    type_id: int

class RoomGet(BaseModel):
    id: int
    number: str
    status: str
    type_name: str # Чтобы сразу видеть "Люкс" вместо ID

class RoomTypeAdd(BaseModel):
    name: str
    description: str
    capacity: int
    price: int

class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    check_in: date
    check_out: date

class BookingGet(BaseModel):
    id: int
    user_fio: str
    room_number: str
    check_in: date
    check_out: date
    total_price: int
    status: str

class BookingUpdateStatus(BaseModel):
    status: str # Например: "cancelled" или "finished"

class ServiceAdd(BaseModel):
    name: str
    price: int

class ServiceOrderAdd(BaseModel):
    booking_id: int
    service_id: int
    quantity: int = 1

class ServiceGet(BaseModel):
    name: str
    price: int

class HotelAdd(BaseModel):
    name: str
    address: str

class HotelGet(BaseModel):
    id: int
    name: str
    address: str
