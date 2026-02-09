from pydantic import BaseModel, Field
from fastapi import FastAPI, Body
from typing import Optional
from datetime import date
from enum import Enum

app = FastAPI()

class Priority(Enum):
    NORMAL = "normal"
    URGENT = "urgent"

class Operation(Enum):
    HEATING = "heating"
    SUPPRESSING = "suppressing"

class Product(BaseModel):
    product_id: str

class Order(BaseModel):
    order_id: str = Field(..., pattern=r'^PO\d{3,5}$')
    deadline: date
    product: Product
    size: Optional[int] = Field(None, ge=10)
    priority: Priority = Priority.NORMAL

class Resource(BaseModel):
    resource_id: str = Field(..., min_length=5, max_length=10)
    capacity: int
    provides: set[Operation]

@app.post("/resources")
async def create_resource(resource_model: Resource):
    print(resource_model.resource_id)
    resource_dict = resource_model.model_dump()
    return resource_dict

@app.put("/resources/{resource_id}")
async def update_resource(resource_id: str, resource_model: Order):
    resource_dict = resource_model.model_dump()
    resource_dict.update({"resource_id": resource_id})
    print(f"[update success] resource {resource_id} successfully updated")
    return resource_dict

@app.post("/jobs/{job_id}")
async def create_job(job_id: str, order_model: Order, resource_model: Resource):
    print(order_model.order_id)
    print(resource_model.resource_id)
    result_dict: dict = {"job_id": job_id}
    result_dict["order"] = order_model.model_dump()
    result_dict["resource"] = resource_model.model_dump()
    return result_dict

@app.put("/{job_id}/size")
async def update_job(order_model: Order, job_id: str, size: int):
    result_dict = order_model.model_dump()
    result_dict["job_id"] = job_id
    result_dict["job_size"] = size
    print(f"[update success] job {job_id} successfully updated")
    return result_dict

@app.put("/{job_id}/length")
async def update_job_length(order_model: Order, job_id: str, length: int = Body(..., ge=10)):
    result_dict = order_model.model_dump()
    result_dict["job_id"] = job_id
    result_dict["job_length"] = length
    print(f"[update success] job {job_id} successfully updated")
    return result_dict


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("request_body:app", reload=True)
