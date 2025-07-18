from pydantic import BaseModel, Field

class Creature(BaseModel):
    name: Field(..., min_length=2)
    country: str
    area: str
    description: str
    aka: str

bad_creature = Creature(
    name="!",
    description="it's a raccoon",
    area="your attic"
)
