from pydantic import BaseModel, Field

class ScanRequest(BaseModel):
    employee_id: str = Field(..., min_length=1)
    order_id: str = Field(..., min_length=1)
    product_id: str = Field(..., min_length=1)

class ScanResponse(BaseModel):
    employee_id: str
    order_id: str
    product_id: str
    scanned_quantity: int
    message: str
