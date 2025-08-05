from fastapi import APIRouter, HTTPException
from model.explorer import Explorer
# import fake.explorer as service
import data.explorer as service
from errors import Missing, Duplicate

router = APIRouter(prefix="/explorer")

@router.get("", tags=["Explorer"])
@router.get("/", tags=["Explorer"])
def get_all() -> list[Explorer]:
    return service.get_all()

@router.get("/{name}", tags=["Explorer"])
def get_one(name: str) -> Explorer:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=201, tags=["Explorer"])
@router.post("/", status_code=201, tags=["Explorer"])
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("/{name}", tags=["Explorer"])
def modify(name: str, explorer: Explorer) -> Explorer:
    try:
        return service.modify(name, explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{name}", tags=["Explorer"])
def delete(name: str) -> bool:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
