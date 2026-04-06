from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import date


class Rental(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    user_id : Optional[int] = Field(foreign_key="user.id")
    car_id : Optional[int] = Field(foreign_key="car.id")
    date : date


class User(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    email: EmailStr
    hash_password : str
    phone_number : str
    driver_license_number : str

    cars : List["Car"] = Relationship(back_populates="users", link_model=Rental)


class Car(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True, index=True)
    category_id : Optional[int] = Field(foreign_key="category.id")
    brand : str
    model : str
    number : str
    available : bool = True

    category : Optional["Category"] = Relationship(back_populates="cars")
    users : List["User"] = Relationship(back_populates="cars", link_model=Rental)


class Category(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    classification : str
    price : float
    
    cars : List["Car"] = Relationship(back_populates="category")


class Location(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    address : str