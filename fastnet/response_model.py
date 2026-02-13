from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

data = {
    '1001': {"job_id": "j001", 'product_id': 'p001'},
    '1002': {'job_id': 'j002', 'product_id': 'p002'},
    '1003': {'job_id': 'j003', 'product_id': 'p003', 'order_id': 'po003'},
    '1004': {'job_id': 'j004', 'product_id': 'p004', 'order_id': 'po004', 'size': 100},
    '1005': {'job_id': 'j005', 'product_id': 'p005', 'order_id': 'po005', 'size': 200, 'due': '2026/12/31'},
}

app = FastAPI()

class JobOutput(BaseModel):
    """
    The output format of Job has to stick to this model
    If not, error will be raised unless attributes have default values.
    """
    job_id: str
    product_id: str
    size: int = 10

class ProductOutput(BaseModel):
    product_id: str
    order_id: str

class OrderOutput(BaseModel):
    order_id: str
    due: str

@app.get("/jobs/{job_id}", response_model=JobOutput)
async def get_job(job_id: str) -> dict:
    return data.get(job_id, {})

@app.get("/products/{product_id}", response_model=ProductOutput, response_model_include={"product_id"})
async def get_product(product_id: str) -> dict:
    return data.get(product_id, {})

@app.get("/orders/{order_id}", response_model=OrderOutput, response_model_exclude={"order_id"})
async def get_order(order_id: str) -> dict:
    return data.get(order_id, {})

@app.get("/size/{job_id}", response_model=JobOutput, response_model_exclude_unset=True)
async def get_size(job_id: str) -> dict:
    return data.get(job_id, {})

@app.get("/jobs", response_model=List[JobOutput])
async def get_all_jobs() -> list[dict]:
    return data.values()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("response_model:app", reload=True)
