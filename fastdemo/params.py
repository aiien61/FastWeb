from fastapi import FastAPI
from typing import Dict
from enum import Enum
import uvicorn

app = FastAPI()


class BurgerSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.get("/users/current")
async def get_current_user():
    return {"user_id": "Current User"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    users: Dict[int, str] = {1: "Alice", 2: "Bob", 3: "Charlie"}
    return {"user_id": user_id, "name": users.get(user_id, "Unknown")}

@app.get("/burger/create/{size}")
async def make_burger(size: BurgerSize):
    return {"burger_size": size.value}


if __name__ == "__main__":
    uvicorn.run("params:app", reload=True)