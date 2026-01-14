from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.database import Base, engine
import app.models  # required

app = FastAPI(title="Windscapes Backend")

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

