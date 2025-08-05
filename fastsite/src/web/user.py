import os
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import User

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as service
else:
    from service import user as service

from errors import Missing, Duplicate

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

router = APIRouter(prefix="/user")

oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")

def unauthed():
    raise HTTPException(
        status_code=401, 
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )

# Redirect to this endpoint for any calling related to oauth2_dep() dependencies
@router.post("/token", tags=["User"])
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get username and password from OAuth form, return access token"""
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={"sub": user.username}, expires=expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/token", tags=["User"])
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Return the current access token"""
    return {"token": token}

# CRUD
@router.get("/", tags=["User"])
def get_all() -> list[User]:
    return service.get_all()

@router.get("/{name}", tags=["User"])
def get_one(name) -> User:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    
@router.post("/", status_code=201, tags=["User"])
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

@router.patch("/", tags=["User"])
def modify(name: str, user: User) -> User:
    try:
        return service.modify(name, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    
@router.delete("/{name}", tags=["User"])
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
