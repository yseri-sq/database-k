from passlib.context import CryptContext

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password : str) -> str:
    return pwd_content.hash(password)

def verify_password(password: str, password_hash : str) -> bool:
    return pwd_content.verify(password, password_hash)