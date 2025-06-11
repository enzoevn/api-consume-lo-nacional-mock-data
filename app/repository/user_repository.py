from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.schemas.models import User
from app.models import Role, UserRegister
from app.services.password_service import PasswordService


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_nickname(self, nickname: str) -> Optional[User]:
        return self.db.query(User).filter(User.nick_name == nickname).first()

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user: UserRegister, skip_password_hash: bool = False) -> User:
        db_user_data = {
            "email": user.email,
            "nick_name": user.nick_name,
            "role": user.role,
            "image": user.image,
            "is_blocked": False,
        }

        if not skip_password_hash:
            if not user.password:
                raise ValueError("Password is required when not skipping hash.")
            db_user_data["hashed_password"] = PasswordService.get_password_hash(
                user.password
            )
        else:
            db_user_data["hashed_password"] = None

        db_user = User(**db_user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: UUID, user_data: dict) -> Optional[User]:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None

        if "password" in user_data:
            user_data["hashed_password"] = PasswordService.get_password_hash(
                user_data.pop("password")
            )

        for field, value in user_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: UUID) -> bool:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_users_by_role(self, role: Role) -> List[User]:
        return self.db.query(User).filter(User.role == role).all()

    def search_users(self, search_term: str) -> List[User]:
        return (
            self.db.query(User)
            .filter(
                (User.email.ilike(f"%{search_term}%"))
                | (User.nick_name.ilike(f"%{search_term}%"))
            )
            .all()
        )

    def block_user(self, user_id: UUID) -> Optional[User]:
        return self.update(user_id, {"is_blocked": True})

    def unblock_user(self, user_id: UUID) -> Optional[User]:
        return self.update(user_id, {"is_blocked": False})
