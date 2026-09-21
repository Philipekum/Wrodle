from fastapi import FastAPI

from app.api.api_router import api_router

app = FastAPI(
    title="Wrodle",
)

app.include_router(api_router)
