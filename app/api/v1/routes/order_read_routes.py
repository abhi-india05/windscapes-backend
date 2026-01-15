from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.order_table import OrderTable
from app.models.ordered_products import OrderedProducts
from app.schemas.order_schema import OrderDetailResponse, OrderedProductView

router = APIRouter()

@router.get("/all")
def show_all_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    orders = db.query(OrderTable).order_by(OrderTable.ordered_at.desc()).all()

    return [
        {
            "order_id": o.order_id,
            "user_id": o.user_id,
            "client_name": o.client_name,
            "status": o.status,
            "total_order_amount": str(o.total_order_amount),
            "ordered_at": str(o.ordered_at),
            "updated_at": str(o.updated_at),
        }
        for o in orders
    ]


@router.get("/{order_id}", response_model=OrderDetailResponse)
def show_order_details_by_id(
    order_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
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
