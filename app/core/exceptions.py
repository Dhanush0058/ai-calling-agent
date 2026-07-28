from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.logger import logger


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    logger.warning(
        f"{request.method} {request.url.path} -> {exc.status_code}: {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )


async def general_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        f"Unhandled exception at {request.method} {request.url.path}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
        },
    )