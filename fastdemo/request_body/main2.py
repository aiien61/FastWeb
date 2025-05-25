from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional, List

import uvicorn

app = FastAPI()


class Address(BaseModel):
    address: str
    postcode: str


class Feature(BaseModel):
    name: str


class User(BaseModel):
    username: str
    id: str = Field(..., min_length=3)
    description: Optional[str] = Field(None, max_length=100)
    address: Address


class Item(BaseModel):
    name: str
    price: float
    features: List[Feature]


@app.put("/carts/{cart_id}")
async def update_cart(cart_id: int, user: User, item: Item, count: int):
    """
    count: Query parameter
    """
    print(user.username)
    print(item.name)
    result_dict: dict = {
        "cart_id": cart_id,
        "user": user.username,
        "item": item.name,
        "price": item.price,
        "count": count
    }
    return result_dict


@app.put("/tobuy/{tobuy_id}")
async def update_tobuy(tobuy_id: int, user: User, item: Item, count: int = Body(..., ge=1)):
    """
    count: Body parameter
    """
    print(user.username)
    print(item.name)
    result_dict: dict = {
        "tobuy_id": tobuy_id,
        "user": user.username,
        "item": item.name,
        "price": item.price,
        "count": count
    }
    return result_dict



if __name__ == "__main__":
    uvicorn.run("main2:app", host="127.0.0.1", port=3000, reload=True)