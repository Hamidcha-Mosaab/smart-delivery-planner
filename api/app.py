from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import routes
from src.utils.logger import setup_logger

app = FastAPI(title="Livraison Intelligente API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    setup_logger()

app.include_router(routes.router, prefix="/api")
