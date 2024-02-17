from fastapi import Depends, APIRouter, HTTPException

from sentinel.utils import get_logger
from sentinel.api.dependencies import get_db
from sentinel.models.base import SessionLocal
from sentinel.api.schemas import hello as hello_schemas
from sentinel.api.services import hello as hello_service

logger = get_logger(__name__)

router = APIRouter(
    prefix="/hello",
    tags=["hello", "example"],
)


@router.get("/", response_model=hello_schemas.Greeting)
def say_hi():
    """Say hi!"""
    return hello_service.say_hi()


@router.post("/", response_model=hello_schemas.Greeting)
def greet(request: hello_schemas.GreetingRequest):
    """Greet someone!"""
    return hello_service.greet(request)


@router.get("/modelitos", response_model=hello_schemas.Greeting)
def probar_modelitos(
    db: SessionLocal = Depends(get_db),
):
    """Modelitos!"""
    return hello_service.probar_modelitos(db)
