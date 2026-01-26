from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from app.models.employee_scan_log import EmployeeScanLog
from app.models.product import Product
from app.models.order_table import OrderTable


def scan_product_service(db: Session, employee_id: str, order_id: str, product_id: str):
    """
    RULES:
    - If scan log doesn't exist -> create with scanned_quantity=1
    - Else -> increment scanned_quantity += 1
    - Before scanning: product.ordered_quantity must be >= 1
    - After scanning: product.ordered_quantity -= 1
    """

    order = db.query(OrderTable).filter(OrderTable.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    product = db.query(Product).filter(Product.product_id == product_id).with_for_update().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.ordered_quantity < 1:
        raise HTTPException(
            status_code=400,
            detail="Cannot scan: ordered_quantity is already 0"
        )

    scan_log = db.query(EmployeeScanLog).filter(
        EmployeeScanLog.employee_id == employee_id,
        EmployeeScanLog.order_id == order_id,
        EmployeeScanLog.product_id == product_id
    ).first()

    try:
        if scan_log is None:
            scan_log = EmployeeScanLog(
                scan_id=str(uuid4()),  # required if scan_id is PK in DB
                employee_id=employee_id,
                order_id=order_id,
                product_id=product_id,
                scanned_quantity=1,
                scanned_at=datetime.utcnow()
            )
            db.add(scan_log)
        else:
            scan_log.scanned_quantity += 1
            scan_log.scanned_at = datetime.utcnow()

        product.ordered_quantity -= 1

        db.commit()
        db.refresh(scan_log)

        return scan_log

    except Exception:
        db.rollback()
        raise
