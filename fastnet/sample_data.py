from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

# option 1 to show samples
class Product(BaseModel):
    product_id: str = Field(..., examples=['AB01'])


class Order(BaseModel):
    order_id: str = Field(..., pattern=r'PO\d{11}', examples=["PO20260211001"])
    size: int = Field(..., min_digits=1, examples=[100])
    products: list[Product] = Field(..., default_factory=list, min_length=1)

# option 2 to show examples
class Job(BaseModel):
    job_id: str = Field(..., min_length=3)
    product_id: str
    order_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "job_id": "J001",
                    "product_id": "AB01",
                    "order_id": "PO20260211001"
                }
            ]

        }
    }

@app.post("/order")
async def create_order(order_model: Order):
    order_dict = order_model.model_dump()
    return order_dict

@app.put("/job")
async def update_job(job_model: Job, machine_id: str = Body(..., examples=['M001'])):
    job_dict = job_model.model_dump()
    job_dict["machine_id"] = machine_id
    return job_dict

@app.put("/product/")
async def update_product(*, product_model: Product, product_id: str = Body(..., examples=["AB02"])):
    product_dict = product_model.model_dump()
    product_dict["product_id"] = product_id
    return product_dict

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sample_data:app", reload=True)