from model import Creature

_creatures: list[Creature] = [
    Creature(
        name="Formosan Black Bear",
        country="TW",
        area="Central and southern mountainous forests",
        description="largest land mammal native to Taiwan",
        aka="White-throated Bear, Ursus thibetanus formosanus"
    ),
    Creature(
        name="Leopard Cat", 
        country="TW", 
        area="central Taiwan", 
        description="native wild feline species",
        aka="Taiwan wild cat"
    )
]

def get_creatures() -> list[Creature]:
    return _creatures
