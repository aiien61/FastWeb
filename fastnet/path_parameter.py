"""
The arguments of path parameters can be auto converted 
to be the arguments for the function
"""
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# The order of functions matters!

@app.get("/users/current")
async def get_current_user():
    return {"user": "current"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user": user_id}

class Size(str, Enum):
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"

@app.get("/parcel/{size}")
async def create_parcel(size: Size):
    return {"parcel size": size}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("path_parameter:app", reload=True)