from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models.incident import Incident
from app.routes import health, incidents

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initial MVP convenience.
    # Replace with Alembic migrations for production.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)


STATIC_DIR = BASE_DIR / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


app.include_router(incidents.router)
app.include_router(health.router)


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):

    with SessionLocal() as db:
        records = db.query(Incident).order_by(Incident.created_at.desc()).all()

        stats = {
            "total": len(records),
            "open": sum(i.status == "Open" for i in records),
            "investigating": sum(i.status == "Investigating" for i in records),
            "resolved": sum(i.status == "Resolved" for i in records),
        }

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={"incidents": records, "stats": stats},
        )
