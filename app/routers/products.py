from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models import (
    CreateProductBase,
    CreateProductContent,
    ProductRequestResponse,
    ProductResponse,
    User,
)
from app.repository.product_repository import ProductRepository
from app.repository.request_repository import RequestRepository
from app.services.auth_service import get_current_active_user

router = APIRouter(tags=["products"])


def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


def get_request_repository(db: Session = Depends(get_db)) -> RequestRepository:
    return RequestRepository(db)


@router.post("/products", status_code=201)
async def create_product(
    product_data: CreateProductBase,
    _: User = Depends(get_current_active_user),
    product_repository: ProductRepository = Depends(get_product_repository),
):
    product = product_repository.create(product_data)
    return {"id": str(product.id)}


@router.get("/products", response_model=List[ProductResponse])
async def search_products(
    name: Optional[str] = None,
    region: Optional[str] = None,
    product_repository: ProductRepository = Depends(get_product_repository),
):
    if name and region:
        # Buscar por nombre y región
        products_by_name = set(product_repository.search_by_name(name))
        products_by_region = set(product_repository.search_by_region(region))
        products = list(products_by_name.intersection(products_by_region))
    elif name:
        # Buscar solo por nombre
        products = product_repository.search_by_name(name)
    elif region:
        # Buscar solo por región
        products = product_repository.search_by_region(region)
    else:
        # Devolver todos los productos
        products = product_repository.get_all()

    # Convertir los productos al formato de respuesta
    return [
        {
            "id": product.id,
            "image": product.image,
            "creationDate": product.creation_date,
            "regions": [region.region_code for region in product.regions],
            "productLanContents": product.product_lan_contents,
        }
        for product in products
    ]


@router.post("/products/{id}/product-content", status_code=201)
async def add_product_content(
    id: UUID,
    content_data: CreateProductContent,
    _: User = Depends(get_current_active_user),
    product_repository: ProductRepository = Depends(get_product_repository),
):
    product = product_repository.add_content(id, content_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"id": str(product.id)}


@router.get("/products/{id}", response_model=ProductResponse)
async def get_product_by_id(
    id: UUID,
    product_repository: ProductRepository = Depends(get_product_repository),
):
    product = product_repository.get_by_id(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Convertir las regiones a una lista de strings
    regions = [region.region_code for region in product.regions]
    return {
        "id": product.id,
        "image": product.image,
        "creationDate": product.creation_date,
        "regions": regions,
        "productLanContents": product.product_lan_contents,
    }


@router.get("/requests/products", response_model=List[ProductRequestResponse])
async def get_product_requests(
    _: User = Depends(get_current_active_user),
    request_repository: RequestRepository = Depends(get_request_repository),
):
    return request_repository.get_product_requests()
