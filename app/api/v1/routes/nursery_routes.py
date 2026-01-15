from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.nursery import Nursery
from app.schemas.nursery_schema import NurseryView

router = APIRouter()

@router.get("/all", response_model=list[NurseryView])
def show_all_nurseries(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    nurseries = db.query(Nursery).all()
    return [NurseryView(nursery_id=n.nursery_id, nursery_name=n.nursery_name) for n in nurseries]
