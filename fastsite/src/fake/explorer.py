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

def get_one_by_name(name: str) -> Explorer | None:
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    return None

def create(explorer: Explorer) -> Explorer:
    """Add an explorer"""
    _explorers.append(explorer)
    return _explorers[-1]

def modify(name: str, explorer: Explorer) -> Explorer:
    """Partially modify an explorer"""
    id_to_modify: int = None

    for id, _explorer in enumerate(_explorers):
        if _explorer.name == name:
            id_to_modify = id
            break
    
    if id_to_modify is None:
        return None
    
    _explorers[id_to_modify] = explorer
    return _explorers[id_to_modify]

def delete(name: str) -> bool:
    """Delete an explorer and return True if it existed"""
    id_to_delete: int = None
    for id, _explorer in enumerate(_explorers):
        if _explorer.name == name:
            id_to_delete = id
            break
    
    if id_to_delete is None:
        return False
    
    _explorers.pop(id_to_delete)
    if name in {_explorer.name for _explorer in _explorers}:
        return True
    
    return False
