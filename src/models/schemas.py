from pydantic import BaseModel, EmailStr

class UserReg(BaseModel):
    name : str
    email : EmailStr
    hash_password : str
    phone_number : str
    driver_lisence_number : int

class UserLog(BaseModel):
    email : EmailStr
    hash_password : str

class UserGet(BaseModel):
    name : str
    email : EmailStr

class UserUpdate(BaseModel):
    email : EmailStr


class CarAdd(BaseModel):
    category_id : int
    brand : str
    model : str
    number : str
    available : bool

class CarUpdate(BaseModel):
    number : str
    avillible : bool

class CarGet(BaseModel):
    brand : str
    model : str
    number : str    


class LocationAdd(BaseModel):
    adress : str

class LocationUpdate(BaseModel):
    adress : str

class LocationGet(BaseModel):
    adress : str