from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional, List
import uvicorn

app = FastAPI()


class Address(BaseModel):
    address: str = Field(..., examples=["123 Main St"])
    postcode: str = Field(..., examples=["100"])


class User(BaseModel):
    username: str = Field(..., min_length=3, examples=["John"])
    description: Optional[str] = Field(None, max_length=100, examples=["This is a description"])
    address: Address


class Item(BaseModel):
    name: str
    price: float

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Foo",
                "price": 99.99
            }]
        }
    }


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):

    result_dict = {
        "id": user_id,
        "username": user.username, 
        "address": user.address, 
        "description": user.description
    }

    return result_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    result_dict = {
        "id": item_id,
        "name": item.name,
        "price": item.price
    }

    return result_dict

@app.put("/cart/{cart_id}")
async def update_cart(*, cart_id: int, buyer: str = Body(..., examples=["admin"]), item: Item, count: int = Body(..., ge=1, examples=[2])):
    result_dict = {
        "id": cart_id,
        "item": item.name,
        "price": item.price,
        "count": count
    }

    return result_dict


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)