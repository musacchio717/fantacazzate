# backend/app/services/user_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.player import Player, Cazzaro
from app.schemas.users import UserCreate, UserUpdate
import hashlib

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def _hash_password(self, password: str) -> str:
        """Hash semplice per ora — sostituiremo con bcrypt quando faremo auth."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, data: UserCreate) -> User:
        # Controlla che email e nickname non esistano già
        if self.db.query(User).filter(User.email == data.email).first():
            raise ValueError("Email già registrata")
        if self.db.query(User).filter(User.nickname == data.nickname).first():
            raise ValueError("Nickname già in uso")

        user = User(
            email=data.email,
            nickname=data.nickname,
            hashed_password=self._hash_password(data.password)
        )
        self.db.add(user)
        self.db.flush()  # ottieni l'id senza committare ancora

        # Crea automaticamente Player e Cazzaro per ogni nuovo User
        player  = Player(user_id=user.id)
        cazzaro = Cazzaro(user_id=user.id, nickname=data.nickname)
        self.db.add(player)
        self.db.add(cazzaro)

        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self) -> list[User]:
        return self.db.query(User).filter(User.is_active == True).all()

    def update_user(self, user_id: int, data: UserUpdate) -> User | None:
        user = self.get_user(user_id)
        if not user:
            return None
        if data.nickname:
            user.nickname = data.nickname
        if data.email:
            user.email = data.email
        self.db.commit()
        self.db.refresh(user)
        return user