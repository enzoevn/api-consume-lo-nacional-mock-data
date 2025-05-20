from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.database import Database
from app.models import (
    CreateThread,
    CreateThreadComment,
    Forum,
    Thread,
    ThreadComment,
    User,
)
from app.routers.users import get_current_user

router = APIRouter(tags=["forums"])


@router.get("/forums", response_model=List[Forum])
def get_all_forums():
    return list(Database.forums.values())


@router.get("/threads/{regionId}", response_model=List[Thread])
def get_threads_by_region(regionId: str):
    if regionId not in Database.forums:
        raise HTTPException(status_code=404, detail="Region not found")

    return [
        thread for thread in Database.threads.values() if thread.regionId == regionId
    ]


@router.post("/threads", status_code=201)
def create_thread(
    thread_data: CreateThread, current_user: User = Depends(get_current_user)
):
    # Verificar que la región existe
    if thread_data.regionId not in Database.forums:
        raise HTTPException(status_code=400, detail="Region not found")

    new_thread = Thread(
        id=uuid4(),
        regionId=thread_data.regionId,
        lan=thread_data.lan,
        title=thread_data.title,
        description=thread_data.description,
        comments=[],
    )

    Database.threads[new_thread.id] = new_thread

    return {"id": str(new_thread.id)}


@router.post("/threads/comments", status_code=201)
def add_thread_comment(
    comment_data: CreateThreadComment, current_user: User = Depends(get_current_user)
):
    try:
        thread_id = comment_data.threadId
        user_id = comment_data.userId
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Verificar que el hilo existe
    if thread_id not in Database.threads:
        raise HTTPException(status_code=404, detail="Thread not found")

    # Verificar que el usuario existe
    if user_id not in Database.users:
        raise HTTPException(status_code=400, detail="User not found")

    # Verificar que el usuario que hace el comentario es el mismo que está autenticado
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Crear el comentario
    new_comment = ThreadComment(
        id=uuid4(),
        threadId=thread_id,
        user=Database.users[user_id],
        content=comment_data.content,
    )

    # Guardar el comentario en la base de datos
    Database.thread_comments[new_comment.id] = new_comment

    # Añadir el comentario al hilo
    Database.threads[thread_id].comments.append(new_comment)

    return {"id": str(new_comment.id)}
