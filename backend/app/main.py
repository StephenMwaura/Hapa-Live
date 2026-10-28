import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from .routes import router
from .seed import seed_events


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_events(db)
    yield


app = FastAPI(title="Hapa Live API", version="0.1.0", lifespan=lifespan)
allowed_origin = os.getenv("HAPA_ALLOWED_ORIGIN", "http://localhost:5173")
app.add_middleware(CORSMiddleware, allow_origins=[allowed_origin], allow_credentials=True, allow_methods=["GET", "POST", "DELETE"], allow_headers=["Content-Type"])
app.include_router(router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "hapa-live-api"}
