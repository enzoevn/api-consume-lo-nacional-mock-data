from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models import (
    LoginResponse,
    ResourceAccess,
    Role,
    User,
    UserLogin,
    UserRegister,
)
from app.repository.resource_repository import ResourceRepository
from app.repository.user_repository import UserRepository
from app.services.auth_service import (
    AuthService,
    get_auth_service,
    get_current_active_user,
    get_current_user,
)

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_resource_repository(db: Session = Depends(get_db)) -> ResourceRepository:
    return ResourceRepository(db)


@router.post("/auth/register", status_code=201)
def register_user(
    user_data: UserRegister,
    user_repository: UserRepository = Depends(get_user_repository),
):
    # Verificar si el correo electrónico o el nombre de usuario ya existen
    if user_repository.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    if user_repository.get_by_nickname(user_data.nick_name):
        raise HTTPException(status_code=400, detail="Nickname already exists")

    # Verificar permisos para roles de empleado
    if user_data.role == "EMPLOYEE":
        raise HTTPException(
            status_code=401, detail="Unauthorized to create EMPLOYEE role"
        )

    # Crear nuevo usuario
    user_repository.create(user_data)

    return {"message": "User created successfully"}


@router.post("/auth/login", response_model=LoginResponse)
def login_user(
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if user.is_blocked:
        raise HTTPException(status_code=401, detail="User is blocked")

    # Generar token
    access_token = auth_service.create_access_token(data={"sub": user.email})

    return LoginResponse(bearer=access_token)


@router.put("/{id}/block", status_code=201)
def block_user(
    id: UUID,
    _: User = Depends(get_current_active_user),
    user_repository: UserRepository = Depends(get_user_repository),
):
    user = user_repository.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_repository.block_user(id)
    return {"message": "User blocked"}


@router.put("/{id}/unblock", status_code=201)
def unblock_user(
    id: UUID,
    _: User = Depends(get_current_active_user),
    user_repository: UserRepository = Depends(get_user_repository),
):
    user = user_repository.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_repository.unblock_user(id)
    return {"message": "User unblocked"}


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[User])
async def get_users(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.role != Role.EMPLOYEE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    users = UserRepository(db).get_all()
    return [
        User(
            id=user.id,
            email=user.email,
            nick_name=user.nick_name,
            role=user.role,
            image=user.image,
            is_blocked=user.is_blocked,
            creation_date=user.creation_date,
        )
        for user in users
    ]


@router.get("/accesses", response_model=List[ResourceAccess])
async def get_resource_accesses(
    _: User = Depends(get_current_active_user),
    resource_repository: ResourceRepository = Depends(get_resource_repository),
):
    return resource_repository.get_all()
