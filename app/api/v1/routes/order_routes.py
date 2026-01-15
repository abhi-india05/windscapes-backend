from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin
from app.schemas.order_schema import (
    OrderCreateRequest,
    OrderCreateResponse,
    OrderAddProductRequest,
    OrderRemoveProductRequest,
    OrderProductActionResponse,
    OrderDetailResponse,
    OrderedProductView,
    OrderUpdateRequest,
)

from app.services.order_service import (
    create_order_service,
    add_product_to_order_service,
    remove_product_from_order_service,
    update_order_basic_details_service,
)

from app.models.order_table import OrderTable
from app.models.ordered_products import OrderedProducts

router = APIRouter()

# Create Order
@router.post("/create", response_model=OrderCreateResponse)
def create_order(
    payload: OrderCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    order = create_order_service(db, payload)
    return OrderCreateResponse(
        order_id=order.order_id,
        status=order.status,
        message="Order created "
    )


# Add/Update product into order
@router.post("/{order_id}/add-product", response_model=OrderProductActionResponse)
def add_product(
    order_id: str,
    payload: OrderAddProductRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    line, order_total = add_product_to_order_service(db, order_id, payload)

    return OrderProductActionResponse(
        order_id=order_id,
        product_id=line.product_id,
        quantity=line.quantity,
        line_total=str(line.total_price),
        order_total=str(order_total),
        message="Product added/updated "
    )


# Remove/Decrease product from order
@router.post("/{order_id}/remove-product")
def remove_product(
    order_id: str,
    payload: OrderRemoveProductRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    order_total = remove_product_from_order_service(db, order_id, payload)

    return {
        "order_id": order_id,
        "product_id": payload.product_id,
        "order_total": str(order_total),
        "message": "Product removed/updated"
    }


# Get full order + products
@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order_details(
    order_id: str,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    order = db.query(OrderTable).filter(OrderTable.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    lines = db.query(OrderedProducts).filter(OrderedProducts.order_id == order_id).all()

    items = [
        OrderedProductView(
            product_id=l.product_id,
            quantity=l.quantity,
            unit_price=str(l.unit_price),
            rate_percentage=str(l.rate_percentage) if l.rate_percentage is not None else None,
            total_price=str(l.total_price)
        )
        for l in lines
    ]

    return OrderDetailResponse(
        order_id=order.order_id,
        user_id=order.user_id,
        client_name=order.client_name,
        status=order.status,
        total_order_amount=str(order.total_order_amount),
        ordered_at=str(order.ordered_at),
        updated_at=str(order.updated_at),
        items=items
    )

@router.patch("/{order_id}/update")
def update_order_details(
    order_id: str,
    payload: OrderUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    order = update_order_basic_details_service(
        db=db,
        order_id=order_id,
        client_name=payload.client_name
    )

    return {
        "message": "Order updated ",
        "order_id": order.order_id,
        "client_name": order.client_name,
        "status": order.status,
        "updated_at": str(order.updated_at)
    }