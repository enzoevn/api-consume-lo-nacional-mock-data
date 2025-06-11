from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.schemas.models import ResourceAccess
from app.models import CreateResourceAccess


class ResourceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, resource_data: CreateResourceAccess) -> ResourceAccess:
        resource = ResourceAccess(
            user_id=resource_data.userId,
            resource_type=resource_data.resourceType,
            resource_id=resource_data.resourceId,
            access_type=resource_data.accessType,
        )
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def get_all(self) -> List[ResourceAccess]:
        return self.db.query(ResourceAccess).all()

    def get_by_id(self, id: UUID) -> Optional[ResourceAccess]:
        return self.db.query(ResourceAccess).filter(ResourceAccess.id == id).first()

    def get_by_user_id(self, user_id: UUID) -> List[ResourceAccess]:
        return (
            self.db.query(ResourceAccess)
            .filter(ResourceAccess.user_id == user_id)
            .all()
        )

    def get_by_resource(
        self, resource_type: str, resource_id: UUID
    ) -> List[ResourceAccess]:
        return (
            self.db.query(ResourceAccess)
            .filter(
                ResourceAccess.resource_type == resource_type,
                ResourceAccess.resource_id == resource_id,
            )
            .all()
        )

    def delete(self, id: UUID) -> bool:
        resource = self.get_by_id(id)
        if not resource:
            return False

        self.db.delete(resource)
        self.db.commit()
        return True
