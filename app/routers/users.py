from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database import Database
from app.models import LoginResponse, ResourceAccess, User, UserLogin, UserRegister

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> User:
    token = credentials.credentials
    user = Database.get_user_by_token(token)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if user.isBloqued:
        raise HTTPException(status_code=401, detail="User is blocked")

    return user


def check_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "EMPLOYEE":
        raise HTTPException(status_code=401, detail="Admin privileges required")
    return user


@router.post("/auth/register", status_code=201)
def register_user(user_data: UserRegister):
    # Verificar si el correo electrónico o el nombre de usuario ya existen
    for user in Database.users.values():
        if user.email == user_data.email or user.nickName == user_data.nickName:
            raise HTTPException(
                status_code=400, detail="Email or nickname already exists"
            )

    # Verificar permisos para roles de empleado
    if user_data.role == "EMPLOYEE":
        raise HTTPException(
            status_code=401, detail="Unauthorized to create EMPLOYEE role"
        )

    # Crear nuevo usuario
    new_user = User(
        id=uuid4(),
        email=user_data.email,
        nickName=user_data.nickName,
        role=user_data.role,
        image=user_data.image,
        isBloqued=False,
        creationDate=Database.users[
            next(iter(Database.users))
        ].creationDate,  # Para mantener consistencia en datos mock
    )

    # Añadir a la base de datos
    Database.users[new_user.id] = new_user

    return {"message": "User created successfully"}


@router.post("/auth/login", response_model=LoginResponse)
def login_user(login_data: UserLogin):
    # En una implementación real, verificaríamos el correo electrónico y la contraseña
    # Aquí simularemos que cualquier correo electrónico válido en la base de datos funciona

    for user in Database.users.values():
        if user.email == login_data.email:
            if user.isBloqued:
                raise HTTPException(status_code=401, detail="User is blocked")

            # Generar token
            token = Database.generate_token(user.id)

            return LoginResponse(bearer=token)

    raise HTTPException(status_code=401, detail="Invalid email or password")


@router.put("/{id}/block", status_code=201)
def block_user(id: str, _: User = Depends(check_admin)):
    try:
        user_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    if user_id not in Database.users:
        raise HTTPException(status_code=404, detail="User not found")

    Database.users[user_id].isBloqued = True

    return {"message": "User blocked"}


@router.put("/{id}/unblock", status_code=201)
def unblock_user(id: str, _: User = Depends(check_admin)):
    try:
        user_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    if user_id not in Database.users:
        raise HTTPException(status_code=404, detail="User not found")

    Database.users[user_id].isBloqued = False

    return {"message": "User unblocked"}


@router.get("/me", response_model=User)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("", response_model=List[User])
def get_users(search: Optional[str] = None, _: User = Depends(check_admin)):
    if not search:
        return list(Database.users.values())

    return [
        user
        for user in Database.users.values()
        if search.lower() in user.email.lower()
        or search.lower() in user.nickName.lower()
    ]


@router.get("/accesses", response_model=List[ResourceAccess])
def get_resource_accesses(_: User = Depends(check_admin)):
    # Devolver los últimos 100 accesos
    return sorted(Database.resource_accesses, key=lambda x: x.accessDate, reverse=True)[
        :100
    ]
