from fastapi import FastAPI
from app.api.v1.endpoints import user_router
from app.middleware.error_handler import ExceptionHandlingMiddleware

app = FastAPI()

app.add_middleware(ExceptionHandlingMiddleware)

app.include_router(user_router.router, prefix="/api/v1")
