from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.database import Database
from app.models import Blog, BlogComment, CreateBlogComment, User
from app.routers.users import get_current_user

router = APIRouter(tags=["blogs"])


@router.post("/blogs/{id}/comments", status_code=201)
def add_blog_comment(
    id: str,
    comment_data: CreateBlogComment,
    current_user: User = Depends(get_current_user),
):
    try:
        blog_id = UUID(id)
        user_id = comment_data.userId
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Verificar que el blog existe
    if blog_id not in Database.blogs:
        raise HTTPException(status_code=404, detail="Blog not found")

    # Verificar que el usuario existe
    if user_id not in Database.users:
        raise HTTPException(status_code=400, detail="User not found")

    # Verificar que el usuario que hace el comentario es el mismo que está autenticado
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Crear comentario
    new_comment = BlogComment(
        id=uuid4(),
        blogId=blog_id,
        user=Database.users[user_id],
        comment=comment_data.comment,
        image=comment_data.image,
        nLikes=0,
    )

    # Guardar comentario en la base de datos
    Database.blog_comments[new_comment.id] = new_comment

    # Añadir comentario al blog
    Database.blogs[blog_id].comments.append(new_comment)

    return {"id": str(new_comment.id)}


@router.post("/blogs/comments/{id}/like", status_code=201)
def like_blog_comment(id: str, current_user: User = Depends(get_current_user)):
    try:
        comment_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid comment ID")

    # Verificar que el comentario existe
    if comment_id not in Database.blog_comments:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Verificar si el usuario ya dio like
    if current_user.id not in Database.user_likes:
        Database.user_likes[current_user.id] = []

    if comment_id in Database.user_likes[current_user.id]:
        raise HTTPException(status_code=400, detail="Already liked")

    # Añadir like
    Database.user_likes[current_user.id].append(comment_id)
    Database.blog_comments[comment_id].nLikes += 1

    return {"message": "Like added"}


@router.get("/blogs/{id}", response_model=Blog)
def get_blog_by_id(id: str):
    try:
        blog_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid blog ID")

    if blog_id not in Database.blogs:
        raise HTTPException(status_code=404, detail="Blog not found")

    return Database.blogs[blog_id]


@router.get("/blogs", response_model=List[Blog])
def search_blogs(name: Optional[str] = None, productId: Optional[str] = None):
    results = list(Database.blogs.values())

    if name:
        # Filtrar por título
        results = [blog for blog in results if name.lower() in blog.title.lower()]

    if productId:
        try:
            product_uuid = UUID(productId)
            # Filtrar por producto
            results = [blog for blog in results if blog.product.id == product_uuid]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid product ID")

    return results
