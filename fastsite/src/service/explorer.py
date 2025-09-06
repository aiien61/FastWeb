import os
from model.explorer import Explorer

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import explorer as data
else:
    from data import explorer as data

def get_all() -> list[Explorer]:
    return data.get_all()

def get_one_by_name(name: str) -> Explorer | None:
    return data.get_one_by_name(name)

def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)

# This just passes the arguments through
# MUST accept both arguments
def modify(name: str, explorer: Explorer) -> Explorer:
    # MUST pass BOTH arguments down to the data layer
    return data.modify(name, explorer)

def delete(name: str) -> bool:
    return data.delete(name)
