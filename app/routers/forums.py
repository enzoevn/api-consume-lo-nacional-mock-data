from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models import (
    CreateThread,
    CreateThreadComment,
    Forum,
    Thread,
    User,
)
from app.repository.forum_repository import ForumRepository
from app.services.auth_service import get_auth_service

router = APIRouter(tags=["forums"])


def get_forum_repository(db: Session = Depends(get_db)) -> ForumRepository:
    return ForumRepository(db)


@router.get("/forums", response_model=List[Forum])
def get_all_forums(
    forum_repository: ForumRepository = Depends(get_forum_repository),
):
    return forum_repository.get_all_forums()


@router.get("/threads/{regionId}", response_model=List[Thread])
def get_threads_by_region(
    regionId: str,
    forum_repository: ForumRepository = Depends(get_forum_repository),
):
    if not forum_repository.get_forum_by_region(regionId):
        raise HTTPException(status_code=404, detail="Region not found")

    return forum_repository.get_threads_by_region(regionId)


@router.post("/threads", status_code=201)
def create_thread(
    thread_data: CreateThread,
    current_user: User = Depends(get_auth_service().get_current_active_user),
    forum_repository: ForumRepository = Depends(get_forum_repository),
):
    thread = forum_repository.create_thread(
        region_id=thread_data.regionId,
        lan=thread_data.lan,
        title=thread_data.title,
        description=thread_data.description,
    )
    if not thread:
        raise HTTPException(status_code=400, detail="Region not found")

    return {"id": str(thread.id)}


@router.post("/threads/comments", status_code=201)
def add_thread_comment(
    comment_data: CreateThreadComment,
    current_user: User = Depends(get_auth_service().get_current_active_user),
    forum_repository: ForumRepository = Depends(get_forum_repository),
):
    # Verificar que el usuario que hace el comentario es el mismo que está autenticado
    if comment_data.userId != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    comment = forum_repository.add_thread_comment(
        comment_data.threadId, comment_data, current_user.id
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Thread not found")

    return {"id": str(comment.id)}
