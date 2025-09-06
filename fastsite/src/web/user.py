import os
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from model.user import User
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
@router.post("/token", tags=["User"], responses={401: {"description": "Incorrect username or password"}})
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Get username and password from OAuth form, return access token"""
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = service.create_access_token(data={"sub": user.username}, expires=expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/token", tags=["User"], responses={401: {"description": "Not authenticated"}})
def get_access_token(token: str = Depends(oauth2_dep)) -> dict[str, str]:
    """Return the current access token"""
    return {"token": token}

# CRUD
@router.get("/", tags=["User"], responses={401: {"description": "User not authenticated"}})
def get_all(token: str = Depends(oauth2_dep)) -> list[User]:
    return service.get_all()

@router.get("/{name}", tags=["User"], responses={401: {"description": "User not authenticated"}, 
                                                 404: {"description": "User not found"}})
def get_one(name) -> User:
    try:
        return service.get_one_by_name(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    
@router.post("/", status_code=201, tags=["User"], responses={409: {"description": "User already exists"}})
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

@router.patch("/", tags=["User"], responses={404: {"description": "User not found"}})
def modify(name: str, user: User) -> User:
    try:
        return service.modify(name, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    
@router.delete("/{name}", tags=["User"], responses={404: {"description": "User not found"}})
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
