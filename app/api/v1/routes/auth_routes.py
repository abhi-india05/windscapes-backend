from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, require_admin
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import UserTable
from app.schemas.auth_schema import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.user_username == payload.user_username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(payload.user_password, user.user_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"user_id": user.user_id, "role": user.role})

    return TokenResponse(
        access_token=token,
        role=user.role,
        user_id=user.user_id
    )


"""
@router.get("/me")
def me(current_user: UserTable = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "user_username": current_user.user_username,
        "role": current_user.role,
        "created_at": current_user.created_at
    }



@router.get("/admin-only")
def admin_only(admin_user: UserTable = Depends(require_admin)):
    return {"message": "Welcome Admin ✅", "admin_id": admin_user.user_id}
"""