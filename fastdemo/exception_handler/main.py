from fastapi import FastAPI, HTTPException, Path, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Optional, List
import uvicorn

app = FastAPI()

users: Dict[str, dict] = {
    'x': {'id': 0},
    'a': {'id': 1, 'username': 'a'},
    'b': {'id': 2, 'username': 'b', 'password': 'passb'},
    'c': {'id': 3, 'username': 'c', 'password': 'passc', 'description': 'default'},
    'd': {'id': 4, 'username': 'd', 'password': 'passd', 'description': 'describer d'},
    'e': {'id': 5, 'username': 'e', 'password': 'passe', 'description': 'describer e', 'fullname': 'easter'},
}

class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    fullname: Optional[str] = None
    description: Optional[str] = None


class UserOutput(UserBase):
    pass


class UserInput(UserBase):
    password: str


class UserNotFoundException(Exception):
    def __init__(self, username: str):
        self.username = username

class ErrorMessage(BaseModel):
    error_code: int
    message: str


@app.post("/users", status_code=201)
async def create_user(user: UserInput):
    user_dict = user.model_dump()
    user_dict.update({"id": 10})
    return user_dict


@app.get("/users/{username}", status_code=200, response_model=UserOutput)
async def get_user(username: str = Path(..., min_length=1)):
    user = users.get(username, None)
    if user:
        return user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{username} not found.')


@app.get("/admins/{admin}", status_code=200, response_model=UserOutput)
async def get_admin(admin: str = Path(..., min_length=1)):
    user = users.get(admin, None)
    if user:
        return user
    
    raise UserNotFoundException(admin)

@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(status_code=404, content={
        "error_code": 404,
        "message": f'"{exc.username}" not found',
        "info": "Please input a valid username"
    })

@app.post("/admin", status_code=201, response_model=UserOutput, responses={
    400: {'model': ErrorMessage},
    401: {'model': ErrorMessage}
})
async def create_admin(admin: UserInput):
    if users.get(admin.username, None):
        error_message = ErrorMessage(error_code=400, message=f'{admin.username} already exists')
        return JSONResponse(status_code=400, content=error_message.model_dump())
    
    admin_dict = admin.model_dump()
    admin_dict.update({'id': 10})
    return admin_dict

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3_000, reload=True)
