from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models import (
    Blog,
    CreateBlog,
    CreateBlogComment,
    Language,
    User,
)
from app.repository.blog_repository import BlogRepository
from app.services.auth_service import get_current_active_user

router = APIRouter(tags=["blogs"])


def get_blog_repository(db: Session = Depends(get_db)) -> BlogRepository:
    return BlogRepository(db)


@router.post("/blogs", status_code=201, operation_id="create_blog")
def create_blog(
    blog_data: CreateBlog,
    current_user: User = Depends(get_current_active_user),
    blog_repository: BlogRepository = Depends(get_blog_repository),
):
    # Verificar que el usuario es un empleado
    if current_user.role != "EMPLOYEE":
        raise HTTPException(
            status_code=403, detail="Solo los empleados pueden crear blogs"
        )

    # Verificar que al menos hay contenido en español
    if not any(content.lan == Language.ES for content in blog_data.contents):
        raise HTTPException(
            status_code=400,
            detail="El blog debe tener al menos el contenido en español",
        )

    # Crear el blog con sus contenidos
    blog = blog_repository.create(blog_data)
    return {"id": str(blog.id)}


@router.post("/blogs/{id}/comments", status_code=201)
def add_blog_comment(
    id: UUID,
    comment_data: CreateBlogComment,
    current_user: User = Depends(get_current_active_user),
    blog_repository: BlogRepository = Depends(get_blog_repository),
):
    # Verificar que el usuario que hace el comentario es el mismo que está autenticado
    if comment_data.userId != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    comment = blog_repository.add_comment(id, comment_data, current_user.id)
    if not comment:
        raise HTTPException(status_code=404, detail="Blog not found")

    return {"id": str(comment.id)}


@router.post("/blogs/comments/{id}/like", status_code=201)
def like_blog_comment(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    blog_repository: BlogRepository = Depends(get_blog_repository),
):
    if not blog_repository.like_comment(id, current_user.id):
        raise HTTPException(status_code=404, detail="Comment not found")

    return {"message": "Like added"}


@router.get("/blogs/{id}", response_model=Blog)
def get_blog_by_id(
    id: UUID,
    blog_repository: BlogRepository = Depends(get_blog_repository),
):
    blog = blog_repository.get_by_id(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


@router.get("/blogs", response_model=List[Blog])
def search_blogs(
    blog_repository: BlogRepository = Depends(get_blog_repository),
):
    blogs = blog_repository.get_all()

    return blogs
