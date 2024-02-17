from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from sentinel import __version__
from sentinel.api.namespaces.hello import \
    router as hello_router
from sentinel.utils import config_logging, get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(
    app: FastAPI,  # pylint: disable=unused-argument, redefined-outer-name
):
    config_logging()
    yield

app = FastAPI(
    title="sentinel API",
    description="""sentinel backend""",
    version=__version__,
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=256)
app.include_router(hello_router)


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    logger.error("Uncaught internal server error", exc_info=True)
    return JSONResponse(
        status_code=500, content={"code": 500, "message": "Internal Server Error"}
    )


@app.get("/healthcheck")
def healthcheck():
    """Reply to health checks requests."""
    return JSONResponse(
        status_code=200, content={"message": "Healthy!", "version": __version__}
    )
