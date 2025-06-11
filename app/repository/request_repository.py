from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.schemas.models import BlogRequest, ProductRequest
from app.models import CreateBlogRequest, CreateProductRequest


class RequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product_request(
        self, request_data: CreateProductRequest, user_id: UUID
    ) -> ProductRequest:
        request = ProductRequest(
            name=request_data.name,
            user_id=user_id,
            image=request_data.image,
            description=request_data.description,
        )
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request

    def get_product_requests(self) -> List[ProductRequest]:
        return self.db.query(ProductRequest).all()

    def create_blog_request(
        self, request_data: CreateBlogRequest, user_id: UUID
    ) -> BlogRequest:
        request = BlogRequest(
            user_id=user_id,
            title=request_data.title,
            description=request_data.description,
            product_id=request_data.productId,
            image=request_data.image,
        )
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request

    def get_blog_requests(self) -> List[BlogRequest]:
        return self.db.query(BlogRequest).all()

    def get_blog_request_by_id(self, request_id: UUID) -> Optional[BlogRequest]:
        return self.db.query(BlogRequest).filter(BlogRequest.id == request_id).first()

    def delete_product_request(self, request_id: UUID) -> bool:
        request = (
            self.db.query(ProductRequest)
            .filter(ProductRequest.id == request_id)
            .first()
        )
        if not request:
            return False

        self.db.delete(request)
        self.db.commit()
        return True

    def delete_blog_request(self, request_id: UUID) -> bool:
        request = self.get_blog_request_by_id(request_id)
        if not request:
            return False

        self.db.delete(request)
        self.db.commit()
        return True
