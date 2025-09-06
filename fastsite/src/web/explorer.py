from fastapi import APIRouter, HTTPException
from model.explorer import Explorer
from service import explorer as service
from errors import Missing, Duplicate

router = APIRouter(prefix="/explorer")

@router.get("", tags=["Explorer"])
@router.get("/", tags=["Explorer"])
def get_all() -> list[Explorer]:
    return service.get_all()

@router.get("/{name}", tags=["Explorer"], responses={404: {"description": "Explorer not found"}})
def get_one(name: str) -> Explorer:
    try:
        return service.get_one_by_name(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=201, tags=["Explorer"], responses={409: {"description": "Explorer already exists"}})
@router.post("/", status_code=201, tags=["Explorer"], responses={409: {"description": "Explorer already exists"}})
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

# The web endpoint must match this signature and pass both arguments.
# The endpoint MUST accept 'name' from the URL and 'explorer' from the body.
@router.patch("/{name}", tags=["Explorer"], responses={404: {"description": "Explorer not found"}})
def modify(name: str, explorer: Explorer) -> Explorer:
    try:
        # MUST pass BOTH arguments down to the service layer.
        return service.modify(name, explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{name}", tags=["Explorer"], responses={404: {"description": "Explorer not found"}})
def delete(name: str) -> bool:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
