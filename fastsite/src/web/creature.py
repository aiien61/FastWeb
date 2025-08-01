from fastapi import APIRouter
from model.creature import Creature
# import fake.creature as service
import data.creature as service

router = APIRouter(prefix="/creature")

@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> Creature:
    return service.get_one(name)

@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)

@router.patch("/{name}")
def modify(name: str) -> Creature:
    creature: Creature = service.get_one(name)
    return service.modify(creature)
