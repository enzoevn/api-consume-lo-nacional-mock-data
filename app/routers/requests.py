from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models import (
    BlogRequestResponse,
    CreateBlogRequest,
    CreateBlogRequestComment,
    CreateProductRequest,
    ProductRequestResponse,
    User,
)
from app.repository.request_repository import RequestRepository
from app.services.auth_service import get_current_active_user

router = APIRouter(prefix="/requests", tags=["requests"])


def get_request_repository(db: Session = Depends(get_db)) -> RequestRepository:
    return RequestRepository(db)


@router.post("/products", status_code=201, operation_id="submit_product_request")
async def submit_product_request(
    request_data: CreateProductRequest,
    current_user: User = Depends(get_current_active_user),
    request_repository: RequestRepository = Depends(get_request_repository),
):
    # Verificar que el usuario que hace la solicitud es el mismo que está autenticado
    if request_data.userId != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    request = request_repository.create_product_request(request_data, current_user.id)
    return {"id": str(request.id)}


@router.get(
    "/products",
    response_model=List[ProductRequestResponse],
    operation_id="get_product_requests_list",
)
async def get_product_requests(
    _: User = Depends(get_current_active_user),
    request_repository: RequestRepository = Depends(get_request_repository),
):
    return request_repository.get_product_requests()


@router.post("/blogs", status_code=201, operation_id="submit_blog_request")
async def submit_blog_request(
    request_data: CreateBlogRequest,
    current_user: User = Depends(get_current_active_user),
    request_repository: RequestRepository = Depends(get_request_repository),
):
    # Verificar que el usuario que hace la solicitud es el mismo que está autenticado
    if request_data.userId != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    request = request_repository.create_blog_request(request_data, current_user.id)
    return {"id": str(request.id)}


@router.get("/blogs", response_model=List[BlogRequestResponse])
async def get_blog_requests(
    _: User = Depends(get_current_active_user),
    request_repository: RequestRepository = Depends(get_request_repository),
):
    return request_repository.get_blog_requests()


@router.post(
    "/blogs/{id}/comment", status_code=201, operation_id="add_comment_to_blog_request"
)
async def add_comment_to_blog_request(
    id: UUID,
    comment_data: CreateBlogRequestComment,
    current_user: User = Depends(get_current_active_user),
    request_repository: RequestRepository = Depends(get_request_repository),
):
    # Verificar que el usuario que hace el comentario es el mismo que está autenticado
    if comment_data.userId != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Verificar que la solicitud de blog existe
    if not request_repository.get_blog_request_by_id(id):
        raise HTTPException(status_code=404, detail="Blog request not found")

    # TODO: Implementar sistema de comentarios para solicitudes de blog
    return {"id": str(id)}
