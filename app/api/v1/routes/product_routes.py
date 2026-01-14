from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin
from app.schemas.product_schema import ProductCreateRequest, ProductCreateResponse
from app.services.product_service import add_product_service

router = APIRouter()

@router.post("/add", response_model=ProductCreateResponse)
def add_product(
    payload: ProductCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)   
):
    product = add_product_service(db, payload)
    return ProductCreateResponse(
        product_id=product.product_id,
        message="Product added successfully "
    )
