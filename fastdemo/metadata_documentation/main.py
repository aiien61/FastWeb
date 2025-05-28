from fastapi import FastAPI
from typing import Dict, List
import uvicorn

title: str = "My FastAPI Demo"
description: str = "This is a fastapi demo"
version: str = "1.0"
terms_of_service: str = "https://google.com"
contact: Dict[str, str] = {
    "name": "Smith",
    "url": "https://google.com",
    "email": "smith@gmail.com"
}

tags_metadata: List[dict] = [
    {
        "name": "Items",
        "description": "APIs for items management",
        "externalDocs": {
            "description": "Items information from external",
            "url": "https://google.com"
        }
    },
    {
        "name": "Users",
        "description": "APIs for users management"
    }
]

app = FastAPI(title=title, 
              description=description, 
              version=version, 
              terms_of_service=terms_of_service,
              contact=contact,
              openapi_tags=tags_metadata,
              openapi_url="/docs/v1/demo.json",
              docs_url="/ui",  # default: docs   If None, users are not allowed to access
              redoc_url="/mydoc")  # default: redoc  If None, users are not allowed to access   

@app.get("/items", tags=["Items"])
async def get_items():
    return {"items": f"Here's all items information"}

@app.get("/users", tags=["Users", "Items"])
async def get_users():
    return {"users": f"Here's all users information"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3_000, reload=True)