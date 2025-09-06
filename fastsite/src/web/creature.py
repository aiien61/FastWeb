from fastapi import APIRouter, HTTPException
from model.creature import Creature
from errors import Missing, Duplicate
from service import creature as service

router = APIRouter(prefix="/creature")

@router.get("/", tags=["Creature"], responses={404: {"description": "Creature not found"}})
def get_all() -> list[Creature]:
    return service.get_all()

# NOTE: The API should return a clean Creature object.
# Tell FastAPI that this endpoint can also return 404
@router.get("/{name}", tags=["Creature"], responses={404: {"description": "Creature not found"}})
def get_one(name: str) -> Creature:
    try:
        return service.get_one_by_name(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("/", status_code=201, tags=["Creature"], responses={409: {"description": "Creature already exists"}})
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        # NOTE: Using 409 (Conflict) is the correct HTTP status code for a duplicate resource.
        raise HTTPException(status_code=409, detail=exc.msg)

@router.patch("/{name}", tags=["Creature"], responses={404: {"description": "Creature not found"}})
def modify(name: str, creature: Creature) -> Creature:
    try:
        return service.modify(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

# NOTE: 204 (No Content) is the standard for a successful DELETE.
# NOTE: A successful DELETE should return no body.
@router.delete("/{name}", status_code=204, tags=["Creature"], responses={404: {"description": "Creature not found"}})
def delete(name: str) -> None:
    try:
        service.delete(name)
        return None
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
