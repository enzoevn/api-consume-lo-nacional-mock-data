from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.schemas.models import Product, ProductLanContent, ProductRegion
from app.models import CreateProductBase, CreateProductContent


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product_data: CreateProductBase) -> Product:
        db_product = Product(
            image=product_data.image,
        )
        self.db.add(db_product)
        self.db.flush()

        # Crear regiones
        for region_code in product_data.regions:
            db_region = ProductRegion(
                product_id=db_product.id,
                region_code=region_code,
            )
            self.db.add(db_region)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all(self) -> List[Product]:
        return self.db.query(Product).all()

    def search_by_name(self, name: str) -> List[Product]:
        return (
            self.db.query(Product)
            .join(Product.product_lan_contents)
            .filter(ProductLanContent.name.ilike(f"%{name}%"))
            .all()
        )

    def search_by_region(self, region: str) -> List[Product]:
        return (
            self.db.query(Product)
            .join(Product.regions)
            .filter(ProductRegion.region_code == region)
            .all()
        )

    def add_content(
        self, product_id: UUID, content_data: CreateProductContent
    ) -> Optional[Product]:
        product = self.get_by_id(product_id)
        if not product:
            return None

        # Verificar si ya existe contenido para ese idioma
        existing_content = (
            self.db.query(ProductLanContent)
            .filter(
                ProductLanContent.product_id == product_id,
                ProductLanContent.lan == content_data.lan.value,
            )
            .first()
        )

        if existing_content:
            # Actualizar contenido existente
            existing_content.name = content_data.name
            existing_content.description = content_data.description
        else:
            # Crear nuevo contenido
            new_content = ProductLanContent(
                product_id=product_id,
                lan=content_data.lan.value,
                name=content_data.name,
                description=content_data.description,
            )
            self.db.add(new_content)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: UUID) -> bool:
        product = self.get_by_id(product_id)
        if not product:
            return False

        self.db.delete(product)
        self.db.commit()
        return True
