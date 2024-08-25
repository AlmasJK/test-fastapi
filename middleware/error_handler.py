from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
import logging

logger = logging.getLogger(__name__)

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"An error occurred: {str(exc)}")
            logger.error(traceback.format_exc())

            error_detail = {
                "type": type(exc).__name__,
                "message": str(exc),
                "trace": traceback.format_exc().splitlines()
            }
            
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "An internal server error occurred.",
                    "errors": [error_detail]
                },
            )
