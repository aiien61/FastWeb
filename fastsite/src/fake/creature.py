from model.creature import Creature
from errors import Missing, Duplicate

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

# def get_one_by_id(id: int) -> Creature:
#     """Return one creature by position"""
#     return _creatures[id]

def get_all() -> list[Creature]:
    """Return all creatures"""
    return _creatures

def get_one_by_name(name: str) -> Creature:
    """Return one creature by name"""
    for _, _creature in enumerate(_creatures):
        if _creature.name == name:
            return _creature
    raise Missing(msg=f"Creature {name} not found.")

def create(creature: Creature) -> Creature:
    """Add a creature"""
    for c in _creatures:
        if c.name == creature.name:
            raise Duplicate(msg=f"Creature {creature.name} already exists.")
    _creatures.append(creature)
    return _creatures[-1]

def modify(name:str, creature: Creature) -> Creature:
    """Partially modify a creature"""
    id_to_modify: int = None

    for id, _creature in enumerate(_creatures):
        if _creature.name == name:
            _creatures[id] = creature
            id_to_modify = id

    if id_to_modify is None:
        raise Missing(msg=f"Creature {name} not found.")
    else:
        return _creatures[id_to_modify]

def delete(name: str) -> bool:
    """Delete a creature and return True if it existed"""
    id_to_delete: int = None
    for id, _creature in enumerate(_creatures):
        if _creature.name == name:
            id_to_delete = id
            break
    if id_to_delete is None:
        raise Missing(msg=f"Creature {name} not found.")
    else:
        _creatures.pop(id_to_delete)
        return True
