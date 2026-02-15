"""
Try
localhost:8000/docs
or
locahost:8000/redoc

"""

from fastapi import FastAPI

demo_info: dict[str, str] = {
    "title": "My FastAPI Demo",
    "description": "This is a demo.",
    "version": "1.0",
    "terms_of_service": "https://google.com",
    "contact": {
        "name": "admin",
        "url": "https://google.com",
        "email": "admin@email.com"
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.9.html"
    },
    "openapi_url": "/myservice/v1/docs.json",
    "redoc_url": "/mydoc",  # change locahost:8000/redoc to locahost:8000/mydoc
    "docs_url": "/mydocs"   # change locahost:8000/docs to locahost:8000/mydocs
    # "docs_url": None   # locahost:8000/docs is not allowed to be accessed

}

tags_metadata: list = [
    {
        "name": "orders",
        "description": "APIs related to orders",
        "externalDocs": {
            "description": "client order document",
            "url": "https://google.com"
        }
    },
    {
        "name": "products",
        "description": "APIs related to products"
    },
    {
        "name": "jobs",
        "description": "APIs related to jobs"
    },
    {
        "name": "resources",
        "description": "APIs related to resources"
    },
    {
        "name": "machines",
        "description": "APIs related to machines"
    },
]

app = FastAPI(openapi_tags=tags_metadata, **demo_info)

@app.get("/orders", tags=["orders"])
async def get_orders():
    return {"order": "PO1001"}

@app.get("/products", tags=["products"])
async def get_products():
    return {"product": "P1001"}

@app.get("/jobs", tags=["jobs"])
async def get_jobs():
    return {"job": "J1001"}

@app.get("/machines", tags=["resources", "machines"])
async def get_machines():
    return {"machine": "M101"}

@app.get("/workers", tags=["resources"])
async def get_workers():
    return {"worker": "H101"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("metadata_document:app", reload=True)
