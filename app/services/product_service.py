from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.nursery import Nursery
from app.schemas.product_schema import ProductCreateRequest
from app.utils.product_id_generator import generate_product_id_8digit

def add_product_service(db: Session, payload: ProductCreateRequest):
    nursery = db.query(Nursery).filter(Nursery.nursery_id == payload.nursery_id).first()
    if not nursery:
        raise HTTPException(status_code=404, detail="Nursery not found")

    product_id = generate_product_id_8digit(payload.nursery_id, payload.size, payload.item_name)

    existing = db.query(Product).filter(Product.product_id == product_id).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Product already exists with product_id={product_id}"
        )

    new_product = Product(
        product_id=product_id,
        nursery_id=payload.nursery_id,
        item_name=payload.item_name.strip(),
        size=payload.size.strip(),
        inventory_quantity=payload.inventory_quantity,
        ordered_quantity=payload.ordered_quantity,
        base_price_per_unit=payload.base_price_per_unit,
        rate_percentage=payload.rate_percentage,
        image_url=str(payload.image_url) if payload.image_url else None
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
