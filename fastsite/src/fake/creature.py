from model.creature import Creature

_creatures: list[object] = [
    Creature(name="Yeti",
             aka="Abominable Snowman",
             country="NPL",
             area="Himalayas",
             description="Hirsute Himalayan"),
    Creature(name="Bigfoot",
             description="Yeti's Cousin Eddie",
             country="US",
             area="*",
             aka="Sasquatch")
]

def get(id: int) -> Creature:
    """Return one creature by position"""
    return _creatures[id]

def get_all() -> list[Creature]:
    """Return all creatures"""
    return _creatures

def get_one(name: str) -> Creature | None:
    """Return one creature by name"""
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None

def create(creature: Creature) -> Creature:
    """Add a creature"""
    _creatures.append(creature)
    return _creatures[-1]

def modify(id: int, creature: Creature) -> Creature:
    """Partially modify a creature"""
    _creatures[id] = creature
    return _creatures[id]

def replace(id: int, creature: Creature) -> Creature:
    """Completely replace a creature"""
    _creatures[id] = creature
    return _creatures[id]

def delete(id: int, creature: Creature) -> bool:
    """Delete a creature and return True if it existed"""
    _creatures.pop(id)
    if creature.name in {_creature.name for _creature in _creatures}:
        return False
    return True
