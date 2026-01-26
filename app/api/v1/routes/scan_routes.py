from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user,require_employee
from app.schemas.scan_schema import ScanRequest, ScanResponse
from app.services.scan_service import scan_product_service

router = APIRouter()

@router.put("/scan", response_model=ScanResponse)
def scan_product(
    payload: ScanRequest,
    db: Session = Depends(get_db),
    user=Depends(require_employee)  
):
    scan_log = scan_product_service(
        db=db,
        employee_id=payload.employee_id,
        order_id=payload.order_id,
        product_id=payload.product_id
    )

    return ScanResponse(
        employee_id=scan_log.employee_id,
        order_id=scan_log.order_id,
        product_id=scan_log.product_id,
        scanned_quantity=scan_log.scanned_quantity,
        message="Scan updated "
    )
