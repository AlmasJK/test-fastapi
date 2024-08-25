from typing import Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Создаем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройки для JWT токенов
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена в минутах

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет совпадение пароля с хешем."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Хеширует пароль."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """Создает JWT токен."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """Декодирует JWT токен."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise Exception("Could not validate credentials")

# Пример для использования
if __name__ == "__main__":
    test_password = "mysecretpassword"
    hashed = get_password_hash(test_password)
    print(f"Hashed password: {hashed}")

    valid = verify_password(test_password, hashed)
    print(f"Password valid: {valid}")

    token = create_access_token(data={"sub": "testuser"})
    print(f"JWT Token: {token}")

    decoded = decode_access_token(token)
    print(f"Decoded token: {decoded}")
