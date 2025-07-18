from pydantic import BaseModel

class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str
    aka: str

thing = Creature(
    name="Leopard Cat", 
    country="TW", 
    area="central Taiwan", 
    description="native wild feline species",
    aka="Taiwan wild cat")

print("Name is", thing.name)
