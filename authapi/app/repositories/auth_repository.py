from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_auth import UserAuthCreate

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User:
        """Получение пользователя по имени пользователя."""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User:
        """Получение пользователя по email."""
        return self.db.query(User).filter(User.email == email).first()

    async def create(self, user_data: UserAuthCreate) -> User:
        """Создание нового пользователя."""
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=user_data.password,  # Хешированный пароль уже передан из сервиса
            is_active=True
        )
        self.db.add(db_user)  # Здесь мы добавляем нового пользователя в сессию
        await self.db.commit()  # Асинхронный коммит требует `await`
        await self.db.refresh(db_user)  # Асинхронный refresh также требует `await`
        return db_user

    def update_password(self, user: User, new_password: str) -> User:
        """Обновление пароля пользователя."""
        user.hashed_password = new_password
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Мягкое удаление пользователя."""
        user.is_deleted = True
        self.db.commit()
