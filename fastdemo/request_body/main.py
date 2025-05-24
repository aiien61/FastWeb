from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import Optional, Dict
import uvicorn


app = FastAPI()

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class UserModel(BaseModel):
    username: str
    description: Optional[str] = "default"
    gender: Gender

@app.post("/users")
async def create_user(user_model: UserModel):
    print(user_model.username)

    user_dict: Dict[str, str] = user_model.model_dump()
    return user_dict

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_model: UserModel):
    print(user_model.username)

    user_dict: Dict[str, str] = user_model.model_dump()
    user_dict.update({"id": user_id})

    return user_dict


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)