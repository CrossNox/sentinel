from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from sentinel.utils import get_logger
from sentinel.api.schemas import hello as hello_schemas

logger = get_logger(__name__)


def say_hi() -> dict:
    return {"message": "hi!"}


def greet(request: hello_schemas.GreetingRequest) -> dict:
    return {"message": f"hi, {request.name}!"}


import random
import string

from sentinel.models.modelitos import ObjA, ObjB, ObjAtoB


def randstr(N: int = 16) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=N))


def probar_modelitos(
    db: Session,
) -> dict:
    bs = [ObjB(string_b=randstr()) for x in range(5)]
    db.add_all(bs)
    db.commit()

    w = ObjA(
        string_a=randstr(),
        objs_a_to_b=[ObjAtoB(extra=10.0, b_id=str(b.id)) for b in bs],
    )
    db.add(w)
    db.commit()

    return {"message": "Probar modelitos"}
