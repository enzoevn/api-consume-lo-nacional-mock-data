import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base
from app.models import AccessDevice, Language, Role

if TYPE_CHECKING:
    pass


class LanguageModel(Base):
    """Model to store languages."""

    __tablename__ = "languages"

    language_code: Mapped[str] = mapped_column(String(5), primary_key=True)

    # Relaciones
    product_lan_contents: Mapped[List["ProductLanContent"]] = relationship(
        back_populates="language", cascade="all, delete-orphan"
    )
    blog_lan_contents: Mapped[List["BlogLanContent"]] = relationship(
        back_populates="language", cascade="all, delete-orphan"
    )


class User(Base):
    """Model to store users."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
    nick_name: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
    role: Mapped[Role] = mapped_column()
    hashed_password: Mapped[str] = mapped_column(String(length=255))
    image: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # Relaciones
    blog_comments: Mapped[List["BlogComment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    product_requests: Mapped[List["ProductRequest"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    blog_requests: Mapped[List["BlogRequest"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    thread_comments: Mapped[List["ThreadComment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    resource_accesses: Mapped[List["ResourceAccess"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Product(Base):
    """Model to store products."""

    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    image: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # Relaciones
    regions: Mapped[List["ProductRegion"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    product_lan_contents: Mapped[List["ProductLanContent"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    blogs: Mapped[List["Blog"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    blog_requests: Mapped[List["BlogRequest"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class ProductRegion(Base):
    """Model to store product regions."""

    __tablename__ = "product_regions"

    product_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    )
    region_code: Mapped[str] = mapped_column(String(length=10), primary_key=True)

    # Relaciones
    product: Mapped[Product] = relationship(back_populates="regions")


class ProductLanContent(Base):
    """Model to store product content in different languages."""

    __tablename__ = "product_lan_contents"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE")
    )
    lan: Mapped[str] = mapped_column(String(5), ForeignKey("languages.language_code"))
    name: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(Text)

    # Relaciones
    product: Mapped[Product] = relationship(back_populates="product_lan_contents")
    language: Mapped[LanguageModel] = relationship(
        back_populates="product_lan_contents"
    )


class Blog(Base):
    """Model to store blogs."""

    __tablename__ = "blogs"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE")
    )
    image: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # Relaciones
    product: Mapped[Product] = relationship(back_populates="blogs")
    blog_lan_contents: Mapped[List["BlogLanContent"]] = relationship(
        back_populates="blog", cascade="all, delete-orphan"
    )
    comments: Mapped[List["BlogComment"]] = relationship(
        back_populates="blog", cascade="all, delete-orphan"
    )


class BlogComment(Base):
    """Model to store blog comments."""

    __tablename__ = "blog_comments"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    blog_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("blogs.id", ondelete="CASCADE")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    comment: Mapped[str] = mapped_column(Text)
    image: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    n_likes: Mapped[int] = mapped_column(default=0)
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # Relaciones
    blog: Mapped[Blog] = relationship(back_populates="comments")
    user: Mapped[User] = relationship(back_populates="blog_comments")


class BlogRequest(Base):
    """Model to store blog requests."""

    __tablename__ = "blog_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    title: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(Text)
    product_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL")
    )
    image: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # Relaciones
    user: Mapped[User] = relationship(back_populates="blog_requests")
    product: Mapped[Product] = relationship(back_populates="blog_requests")


class ProductRequest(Base):
    """Model to store product requests."""

    __tablename__ = "product_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(length=255))
    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    image: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # Relaciones
    user: Mapped[User] = relationship(back_populates="product_requests")


class ResourceAccess(Base):
    """Model to store resource accesses."""

    __tablename__ = "resource_accesses"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    resource_type: Mapped[str] = mapped_column(String(length=255), nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    access_type: Mapped[str] = mapped_column(String(length=255), nullable=False)
    access_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC), nullable=False
    )
    device_type: Mapped[AccessDevice] = mapped_column()

    # Relaciones
    user: Mapped[User] = relationship(back_populates="resource_accesses")


class Forum(Base):
    """Model to store forums."""

    __tablename__ = "forums"

    region_id: Mapped[str] = mapped_column(String(length=10), primary_key=True)
    region_name: Mapped[str] = mapped_column(String(length=255))

    # Relaciones
    threads: Mapped[List["Thread"]] = relationship(
        back_populates="forum", cascade="all, delete-orphan"
    )


class Thread(Base):
    """Model to store threads."""

    __tablename__ = "threads"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    region_id: Mapped[str] = mapped_column(
        String(length=10), ForeignKey("forums.region_id", ondelete="CASCADE")
    )
    lan: Mapped[Language] = mapped_column()
    title: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # Relaciones
    forum: Mapped[Forum] = relationship(back_populates="threads")
    comments: Mapped[List["ThreadComment"]] = relationship(
        back_populates="thread", cascade="all, delete-orphan"
    )


class ThreadComment(Base):
    """Model to store thread comments."""

    __tablename__ = "thread_comments"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    thread_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("threads.id", ondelete="CASCADE")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    content: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # Relaciones
    thread: Mapped[Thread] = relationship(back_populates="comments")
    user: Mapped[User] = relationship(back_populates="thread_comments")


class BlogLanContent(Base):
    """Model to store blog content in different languages."""

    __tablename__ = "blog_lan_contents"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    blog_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("blogs.id", ondelete="CASCADE")
    )
    lan: Mapped[str] = mapped_column(String(5), ForeignKey("languages.language_code"))
    title: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(Text)

    # Relaciones
    blog: Mapped[Blog] = relationship(back_populates="blog_lan_contents")
    language: Mapped[LanguageModel] = relationship(back_populates="blog_lan_contents")
