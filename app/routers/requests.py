from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.database import Database
from app.models import (
    BlogRequest,
    CreateBlogRequest,
    CreateBlogRequestComment,
    CreateProductRequest,
    ProductRequest,
    User,
)
from app.routers.users import check_admin, get_current_user

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("/products", status_code=201)
def submit_product_request(
    request_data: CreateProductRequest, current_user: User = Depends(get_current_user)
):
    try:
        user_id = request_data.userId
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Verificar que el usuario existe
    if user_id not in Database.users:
        raise HTTPException(status_code=400, detail="User not found")

    # Verificar que el usuario que hace la solicitud es el mismo que está autenticado
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    new_request = ProductRequest(
        id=uuid4(),
        name=request_data.name,
        user=Database.users[user_id],
        image=request_data.image,
        description=request_data.description,
    )

    Database.product_requests[new_request.id] = new_request

    return {"id": str(new_request.id)}


@router.get("/products", response_model=List[ProductRequest])
def get_product_requests(_: User = Depends(check_admin)):
    return list(Database.product_requests.values())


@router.post("/blogs", status_code=201)
def submit_blog_request(
    request_data: CreateBlogRequest, current_user: User = Depends(get_current_user)
):
    try:
        user_id = request_data.userId
        product_id = request_data.productId
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Verificar que el usuario existe
    if user_id not in Database.users:
        raise HTTPException(status_code=400, detail="User not found")

    # Verificar que el producto existe
    if product_id not in Database.products:
        raise HTTPException(status_code=400, detail="Product not found")

    # Verificar que el usuario que hace la solicitud es el mismo que está autenticado
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    new_request = BlogRequest(
        id=uuid4(),
        user=Database.users[user_id],
        title=request_data.title,
        description=request_data.description,
        product=Database.products[product_id],
        image=request_data.image,
    )

    Database.blog_requests[new_request.id] = new_request

    return {"id": str(new_request.id)}


@router.get("/blogs", response_model=List[BlogRequest])
def get_blog_requests(_: User = Depends(check_admin)):
    return list(Database.blog_requests.values())


@router.post("/blogs/{id}/comment", status_code=201)
def add_comment_to_blog_request(
    id: str,
    comment_data: CreateBlogRequestComment,
    current_user: User = Depends(get_current_user),
):
    try:
        blog_id = UUID(id)
        user_id = comment_data.userId
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Verificar que la solicitud de blog existe
    if blog_id not in Database.blog_requests:
        raise HTTPException(status_code=404, detail="Blog request not found")

    # Verificar que el usuario existe
    if user_id not in Database.users:
        raise HTTPException(status_code=400, detail="User not found")

    # Verificar que el usuario que hace el comentario es el mismo que está autenticado
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # En una implementación real, aquí guardaríamos el comentario en la base de datos
    # Para este mock, solo retornamos un ID simulado

    return {"id": str(uuid4())}
