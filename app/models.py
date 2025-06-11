from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Role(str, Enum):
    USER = "USER"
    EMPLOYEE = "EMPLOYEE"


class Language(str, Enum):
    ES = "es-ES"
    EN = "en-US"


class AccessDevice(str, Enum):
    WEB = "WEB"
    MOBILE = "MOBILE"


class User(BaseModel):
    id: UUID = uuid4()
    email: str
    nick_name: str
    role: Role
    image: Optional[str] = None
    is_blocked: bool = False
    creation_date: datetime = Field(default_factory=datetime.now, alias="creation_date")


class ProductLanContent(BaseModel):
    lan: Language
    name: str
    description: str


class Product(BaseModel):
    id: UUID = uuid4()
    image: Optional[str] = None
    creation_date: datetime = Field(default_factory=datetime.now, alias="creation_date")
    regions: List[str]
    product_lan_contents: List[ProductLanContent] = Field(
        default_factory=list, alias="product_lan_contents"
    )


class BlogComment(BaseModel):
    id: UUID = uuid4()
    blog_id: UUID = Field(alias="blog_id")
    user: User
    comment: str
    image: Optional[str] = None
    n_likes: int = 0
    creation_date: datetime = Field(default_factory=datetime.now, alias="creation_date")


class BlogLanContent(BaseModel):
    blog_id: UUID = Field(alias="blog_id")
    lan: Language
    title: str
    description: str


class Blog(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    product_id: UUID = Field(alias="product_id")
    image: Optional[str] = None
    blog_lan_contents: List[BlogLanContent] = Field(
        default_factory=list, alias="blog_lan_contents"
    )
    comments: List[BlogComment] = Field(default_factory=list)
    creation_date: datetime = Field(default_factory=datetime.now, alias="creation_date")

    class Config:
        from_attributes = True
        populate_by_name = True


class ProductRequest(BaseModel):
    id: UUID = uuid4()
    name: str
    user: User
    image: Optional[str] = None
    description: str
    creationDate: datetime = datetime.now()


class BlogRequest(BaseModel):
    id: UUID = uuid4()
    user: User
    title: str
    description: str
    product: Product
    image: Optional[str] = None
    creationDate: datetime = datetime.now()


class ResourceAccess(BaseModel):
    id: UUID = uuid4()
    userId: UUID
    resourceType: str
    resourceId: UUID
    accessType: str
    accessDate: datetime = datetime.now()
    deviceType: AccessDevice


class CreateResourceAccess(BaseModel):
    userId: UUID
    resourceType: str
    resourceId: UUID
    accessType: str
    deviceType: AccessDevice


class Forum(BaseModel):
    regionId: str
    regionName: str


class ThreadComment(BaseModel):
    id: UUID = uuid4()
    threadId: UUID
    user: User
    content: str
    creationDate: datetime = datetime.now()


class Thread(BaseModel):
    id: UUID = uuid4()
    regionId: str
    lan: Language
    title: str
    description: str
    comments: List[ThreadComment] = []
    creationDate: datetime = datetime.now()


class Error(BaseModel):
    message: str


# Modelos adicionales para solicitudes de entrada
class UserRegister(BaseModel):
    email: str
    nick_name: str
    role: Role
    password: str
    image: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    bearer: str


class CreateProductBase(BaseModel):
    image: str
    regions: List[str]


class CreateProductContent(BaseModel):
    lan: Language
    name: str
    description: str


class CreateBlogComment(BaseModel):
    userId: UUID
    comment: str
    image: Optional[str] = None


class CreateProductRequest(BaseModel):
    name: str
    userId: UUID
    image: Optional[str] = None
    description: str


class CreateBlogRequest(BaseModel):
    title: str
    productId: UUID
    userId: UUID
    image: Optional[str] = None
    description: str


class CreateBlogRequestComment(BaseModel):
    blogId: UUID
    userId: UUID
    comment: str
    image: Optional[str] = None


class CreateThread(BaseModel):
    regionId: str
    lan: Language
    title: str
    description: str


class CreateThreadComment(BaseModel):
    threadId: UUID
    userId: UUID
    content: str


class ProductRequestResponse(BaseModel):
    id: UUID
    name: str
    userId: UUID
    image: Optional[str] = None
    description: str
    creationDate: datetime

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: UUID
    image: Optional[str] = None
    creationDate: datetime
    regions: List[str]
    productLanContents: List[ProductLanContent] = []

    class Config:
        from_attributes = True


class BlogRequestResponse(BaseModel):
    id: UUID
    userId: UUID
    title: str
    description: str
    productId: UUID
    image: Optional[str] = None
    creationDate: datetime

    class Config:
        from_attributes = True


class CreateBlog(BaseModel):
    productId: UUID
    image: Optional[str] = None
    contents: List[BlogLanContent]
