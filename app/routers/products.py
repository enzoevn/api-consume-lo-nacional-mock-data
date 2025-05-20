from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.database import Database
from app.models import (
    CreateProductBase,
    CreateProductContent,
    Product,
    ProductLanContent,
    ProductRequest,
)
from app.routers.users import check_admin

router = APIRouter(tags=["products"])


@router.post("/products", status_code=201)
def create_product(product_data: CreateProductBase, admin=Depends(check_admin)):
    new_product = Product(
        id=uuid4(),
        image=product_data.image,
        regions=product_data.regions,
        productLanContents=[],
    )

    Database.products[new_product.id] = new_product

    return {"id": str(new_product.id)}


@router.get("/products", response_model=List[Product])
def search_products(name: Optional[str] = None, region: Optional[str] = None):
    results = list(Database.products.values())

    if name:
        # Filtrar por nombre en cualquier idioma
        results = [
            product
            for product in results
            if any(
                name.lower() in content.name.lower()
                for content in product.productLanContents
            )
        ]

    if region:
        # Filtrar por región
        results = [product for product in results if region in product.regions]

    return results


@router.post("/products/{id}/product-content", status_code=201)
def add_product_content(
    id: str, content_data: CreateProductContent, admin=Depends(check_admin)
):
    try:
        product_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    if product_id not in Database.products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = Database.products[product_id]
    product_content = ProductLanContent(**content_data.dict())

    # Verificar si ya existe contenido para ese idioma
    for i, content in enumerate(product.productLanContents):
        if content.lan == content_data.lan:
            # Actualizar el contenido existente
            product.productLanContents[i] = product_content
            return {"id": str(product_id)}

    # Añadir nuevo contenido
    product.productLanContents.append(product_content)

    return {"id": str(product_id)}


@router.get("/products/{id}", response_model=Product)
def get_product_by_id(id: str):
    try:
        product_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    if product_id not in Database.products:
        raise HTTPException(status_code=404, detail="Product not found")

    return Database.products[product_id]


@router.get("/requests/products", response_model=List[ProductRequest])
def get_product_requests(admin=Depends(check_admin)):
    return list(Database.product_requests.values())
