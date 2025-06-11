from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.db.schemas.models import Blog, BlogComment, BlogLanContent, User
from app.models import CreateBlog, CreateBlogComment


class BlogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, blog_id: UUID) -> Optional[Blog]:
        return (
            self.db.query(Blog)
            .options(joinedload(Blog.blog_lan_contents), joinedload(Blog.comments))
            .filter(Blog.id == blog_id)
            .first()
        )

    def get_all(
        self,
    ) -> List[Blog]:
        return (
            self.db.query(Blog)
            .options(joinedload(Blog.blog_lan_contents), joinedload(Blog.comments))
            .all()
        )

    def search_by_title(self, title: str) -> List[Blog]:
        return (
            self.db.query(Blog)
            .join(BlogLanContent)
            .filter(BlogLanContent.title.ilike(f"%{title}%"))
            .all()
        )

    def search_by_product(self, product_id: UUID) -> List[Blog]:
        return self.db.query(Blog).filter(Blog.product_id == product_id).all()

    def add_comment(
        self, blog_id: UUID, comment_data: CreateBlogComment, user_id: UUID
    ) -> Optional[BlogComment]:
        blog = self.get_by_id(blog_id)
        if not blog:
            return None

        new_comment = BlogComment(
            blog_id=blog_id,
            user_id=user_id,
            comment=comment_data.comment,
            image=comment_data.image,
            n_likes=0,
        )
        self.db.add(new_comment)
        self.db.commit()
        self.db.refresh(new_comment)
        return new_comment

    def like_comment(self, comment_id: UUID, user_id: UUID) -> bool:
        comment = (
            self.db.query(BlogComment).filter(BlogComment.id == comment_id).first()
        )
        if not comment:
            return False

        comment.n_likes += 1
        self.db.commit()
        return True

    def create(self, blog_data: CreateBlog) -> Blog:
        # Crear el blog base
        blog = Blog(
            product_id=blog_data.productId,
            image=blog_data.image,
        )
        self.db.add(blog)
        self.db.flush()  # Para obtener el ID del blog

        # Crear los contenidos en diferentes idiomas
        for content in blog_data.contents:
            blog_content = BlogLanContent(
                blog_id=blog.id,
                lan=content.lan,
                title=content.title,
                description=content.description,
            )
            self.db.add(blog_content)

        self.db.commit()
        self.db.refresh(blog)
        return blog

    def delete(self, blog_id: UUID) -> bool:
        blog = self.get_by_id(blog_id)
        if not blog:
            return False

        self.db.delete(blog)
        self.db.commit()
        return True

    def get_blog_lan_contents(self, blog_id: UUID) -> List[BlogLanContent]:
        return (
            self.db.query(BlogLanContent)
            .filter(BlogLanContent.blog_id == blog_id)
            .all()
        )

    def get_blog_comments(self, blog_id: UUID) -> List[BlogComment]:
        return self.db.query(BlogComment).filter(BlogComment.blog_id == blog_id).all()

    def get_user_by_blog_id(self, user_id: UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
