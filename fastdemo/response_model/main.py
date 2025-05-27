from fastapi import FastAPI
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

class UserOutput(BaseModel):
    id: int
    username: str
    description: Optional[str] = "default"

@app.get("/users/{username}", response_model=UserOutput)
async def get_user(username: str):
    return users.get(username, {})


@app.get("/admins/{admin}", response_model=UserOutput, response_model_include={"id", "username"})
async def get_admin(admin: str):
    return users.get(admin, {})


@app.get("/clients/{client}", response_model=UserOutput, response_model_exclude={"id", "username"})
async def get_client(client: str):
    return users.get(client, {})

@app.get("/members/{member}", response_model=UserOutput, response_model_exclude_unset=True)
async def get_member(member: str):
    return users.get(member, {})


@app.get("/users", response_model=List[UserOutput])
async def get_users():
    qualified_users = {k: v for k, v in users.items() if 'username' in v}
    return qualified_users.values()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3_000, reload=True)