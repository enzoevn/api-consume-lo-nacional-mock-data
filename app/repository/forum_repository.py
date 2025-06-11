from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.schemas.models import Forum, Thread, ThreadComment
from app.models import CreateThreadComment, Language


class ForumRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_forums(self) -> List[Forum]:
        return self.db.query(Forum).all()

    def get_forum_by_region(self, region_id: str) -> Optional[Forum]:
        return self.db.query(Forum).filter(Forum.region_id == region_id).first()

    def get_threads_by_region(self, region_id: str) -> List[Thread]:
        return self.db.query(Thread).filter(Thread.region_id == region_id).all()

    def create_thread(
        self,
        region_id: str,
        lan: Language,
        title: str,
        description: str,
    ) -> Optional[Thread]:
        forum = self.get_forum_by_region(region_id)
        if not forum:
            return None

        thread = Thread(
            region_id=region_id,
            lan=lan,
            title=title,
            description=description,
        )
        self.db.add(thread)
        self.db.commit()
        self.db.refresh(thread)
        return thread

    def add_thread_comment(
        self, thread_id: UUID, comment_data: CreateThreadComment, user_id: UUID
    ) -> Optional[ThreadComment]:
        thread = self.db.query(Thread).filter(Thread.id == thread_id).first()
        if not thread:
            return None

        comment = ThreadComment(
            thread_id=thread_id,
            user_id=user_id,
            content=comment_data.content,
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_thread_by_id(self, thread_id: UUID) -> Optional[Thread]:
        return self.db.query(Thread).filter(Thread.id == thread_id).first()

    def delete_thread(self, thread_id: UUID) -> bool:
        thread = self.get_thread_by_id(thread_id)
        if not thread:
            return False

        self.db.delete(thread)
        self.db.commit()
        return True

    def delete_comment(self, comment_id: UUID) -> bool:
        comment = (
            self.db.query(ThreadComment).filter(ThreadComment.id == comment_id).first()
        )
        if not comment:
            return False

        self.db.delete(comment)
        self.db.commit()
        return True
