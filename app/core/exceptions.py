from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc):
        return JSONResponse(
            status_code=422,
            content={"error": "Invalid request data"}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc):
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )