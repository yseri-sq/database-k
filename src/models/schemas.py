from pydantic import BaseModel, EmailStr

class UserReg(BaseModel):
    name : str
    email : EmailStr
    hash_password : str
    phone_number : str
    driver_license_number : str

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
    available : bool

class CarGet(BaseModel):
    brand : str
    model : str
    number : str    


class LocationAdd(BaseModel):
    address : str

class LocationUpdate(BaseModel):
    address : str

class LocationGet(BaseModel):
    address : str