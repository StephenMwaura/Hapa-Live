import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

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

# In production, serve Vite's built files from the same host as the API.
FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if FRONTEND_DIST.is_dir():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend-assets")

    @app.get("/{path:path}", include_in_schema=False)
    def serve_frontend(path: str):
        if path == "api" or path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")

        requested_file = (FRONTEND_DIST / path).resolve()
        if requested_file.is_relative_to(FRONTEND_DIST.resolve()) and requested_file.is_file():
            if requested_file.name == "index.html":
                return frontend_index_response(requested_file)
            return FileResponse(requested_file)
        return frontend_index_response(FRONTEND_DIST / "index.html")


def frontend_index_response(index_file: Path) -> HTMLResponse:
    token = json.dumps(os.getenv("HAPA_CLOUDFLARE_TOKEN", ""))
    html = index_file.read_text(encoding="utf-8")
    html = html.replace(json.dumps("__HAPA_CLOUDFLARE_TOKEN__"), token)
    return HTMLResponse(content=html)
