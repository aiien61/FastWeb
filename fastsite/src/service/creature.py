from model.creature import Creature
import fake.creature as data

def get(id: int) -> Creature:
    return data.get(id)

def get_all() -> list[Creature]:
    return data.get_all()

def get_one(name: str) -> Creature | None:
    return data.get_one(name)

def create(creature: Creature) -> Creature:
    return data.create(creature)

def replace(id: int, creature: Creature) -> Creature:
    return data.replace(id, creature)

def modify(id: int, creature: Creature) -> Creature:
    return data.modify(id, creature)

def delete(id: int, creature: Creature) -> bool:
    return data.delete(id, creature)
