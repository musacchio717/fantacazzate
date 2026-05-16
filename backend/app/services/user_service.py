from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.auth import hash_password, verify_password, create_access_token
import random
import string

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_username(self, base: str) -> str:
        username = base
        counter = 1
        while self.db.query(User).filter(User.username == username).first():
            username = f"{base}_{counter}"
            counter += 1
        return username

    def _generate_password(self, length: int = 5) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def create_user(self, nickname: str, role: str = UserRole.OBSERVER) -> dict:
        base_username = nickname.lower().replace(" ", "_")
        username = self._generate_username(base_username)
        password = self._generate_password(5)
        hashed = hash_password(password)
        user = User(
            username=username,
            nickname=nickname,
            hashed_password=hashed,
            role=role,
            is_active=True
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return {
            "user_id": user.id,
            "username": username,
            "password": password,
            "nickname": nickname,
            "role": role
        }

    def login(self, username: str, password: str) -> dict:
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid username or password")
        if not user.is_active:
            raise ValueError("User is not active")
        token = create_access_token(user.id, user.username, user.role)
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": user.username,
            "role": user.role
        }

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def list_all_users(self) -> list[User]:
        return self.db.query(User).all()