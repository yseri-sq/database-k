from datetime import date
from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    FIO: str
    email: EmailStr
    phone: str
    passport: str
    date_birth: date
    
    bookings: List["Booking"] = Relationship(back_populates="user")

class Hotel(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    address: str
    
    rooms: List["Room"] = Relationship(back_populates="hotel")

class RoomTypes(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    description: str
    capacity: int
    price: int
    
    rooms: List["Room"] = Relationship(back_populates="room_type")

class Room(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    number: str
    status: str = "free"
    
    hotel_id: int = Field(foreign_key="hotel.id")
    hotel: Hotel = Relationship(back_populates="rooms")
    
    type_id: int = Field(foreign_key="roomtypes.id")
    room_type: RoomTypes = Relationship(back_populates="rooms")
    
    bookings: List["Booking"] = Relationship(back_populates="room")

class Booking(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    check_in: date
    check_out: date
    total_price: int
    status: str = "confirmed"
    
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="bookings")
    
    room_id: int = Field(foreign_key="room.id")
    room: Room = Relationship(back_populates="bookings")
    
    service_orders: List["ServiceOrder"] = Relationship(back_populates="booking")

class Service(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    price: int
    
    orders: List["ServiceOrder"] = Relationship(back_populates="service")

class ServiceOrder(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    quantity: int = 1
    
    booking_id: int = Field(foreign_key="booking.id")
    booking: Booking = Relationship(back_populates="service_orders")
    
    service_id: int = Field(foreign_key="service.id")
    service: Service = Relationship(back_populates="orders")
