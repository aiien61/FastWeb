from model.explorer import Explorer

_explorers: list[object] = [
    Explorer(name="Claude Hande",
             country="FR",
             description="Scarce during full moons"),
    Explorer(name="Noah Weiser",
             country="DE",
             description="Myopic machete man")
]

def get_all() -> list[Explorer]:
    """Return all explorers"""
    return _explorers

def get_one(name: str) -> Explorer | None:
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    return None

def create(explorer: Explorer) -> Explorer:
    """Add an explorer"""
    _explorers.append(explorer)
    return _explorers[-1]

def modify(id: int, explorer: Explorer) -> Explorer:
    """Partially modify an explorer"""
    _explorers[id] = explorer
    return _explorers[id]

def replace(id: int, explorer: Explorer) -> Explorer:
    """Completely replace an explorer"""
    _explorers[id] = explorer
    return _explorers[id]

def delete(id: int, explorer: Explorer) -> bool:
    """Delete an explorer and return True if it existed"""
    _explorers.pop(id)
    if explorer.name in {_explorer.name for _explorer in _explorers}:
        return True
    return False
