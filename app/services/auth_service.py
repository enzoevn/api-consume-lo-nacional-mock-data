from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.db.connection import get_db
from app.db.schemas.auth import TokenData
from app.models import User as UserModel
from app.repository.user_repository import UserRepository
from app.services.password_service import PasswordService

settings = get_settings()
security = HTTPBearer(auto_error=False)


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
        user = self.user_repository.get_by_email(email)
        if not user or not user.hashed_password:
            return None
        if not PasswordService.verify_password(password, user.hashed_password):
            return None
        return UserModel(
            id=user.id,
            email=user.email,
            nick_name=user.nick_name,
            role=user.role,
            image=user.image,
            is_blocked=user.is_blocked,
            creation_date=datetime.now(),
        )

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    async def get_current_user(
        self, token: HTTPAuthorizationCredentials = Depends(security)
    ) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token.credentials, settings.secret_key, algorithms=[settings.algorithm]
            )
            email = payload.get("sub")
            if not email or not isinstance(email, str):
                raise credentials_exception
            token_data = TokenData(email=email)
            if not token_data.email:
                raise credentials_exception
            user = self.user_repository.get_by_email(token_data.email)
            if user is None:
                raise credentials_exception
            return UserModel(
                id=user.id,
                email=user.email,
                nick_name=user.nick_name,
                role=user.role,
                image=user.image,
                is_blocked=user.is_blocked,
                creation_date=datetime.now(),
            )
        except JWTError:
            raise credentials_exception

    async def get_current_active_user(
        self, current_user: UserModel = Depends(get_current_user)
    ) -> UserModel:
        if current_user.is_blocked:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    token: HTTPAuthorizationCredentials = Depends(security),
) -> UserModel:
    return await auth_service.get_current_user(token)


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if current_user.is_blocked:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
