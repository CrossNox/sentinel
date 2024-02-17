from pydantic import BaseModel


class Greeting(BaseModel):
    message: str


class GreetingRequest(BaseModel):
    name: str


