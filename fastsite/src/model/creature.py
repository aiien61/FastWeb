from pydantic import BaseModel

class Creature(BaseModel):
    name: str
    country: str
    area: str | None = None
    description: str
    aka: str | None = None
