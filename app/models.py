from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel


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
    nickName: str
    role: Role
    image: Optional[str] = None
    isBloqued: bool = False
    creationDate: datetime = datetime.now()


class ProductLanContent(BaseModel):
    lan: Language
    name: str
    description: str


class Product(BaseModel):
    id: UUID = uuid4()
    image: Optional[str] = None
    creationDate: datetime = datetime.now()
    regions: List[str]
    productLanContents: List[ProductLanContent] = []


class BlogComment(BaseModel):
    id: UUID = uuid4()
    blogId: UUID
    user: User
    comment: str
    image: Optional[str] = None
    nLikes: int = 0
    creationDate: datetime = datetime.now()


class Blog(BaseModel):
    id: UUID = uuid4()
    product: Product
    lan: Language
    title: str
    description: str
    image: Optional[str] = None
    comments: List[BlogComment] = []
    creationDate: datetime = datetime.now()


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
    user: Optional[User] = None
    accessDate: datetime = datetime.now()
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
    nickName: str
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
