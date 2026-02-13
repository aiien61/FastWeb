from fastapi import FastAPI, Path, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# alternative: acceptable error handler for simple, convenient handling

order_data: dict = {
    'PO1001': {
        "order_id": "PO1001",
        "due_date": "20261201",
        "products": [
            "P1001"
        ],
        "quantity": 10
    }
}

class OrderBase(BaseModel):
    order_id: Optional[str] = None
    due_date: str
    products: list[str]
    quantity: int

class OrderIn(OrderBase):
    role: str
    password: str

class OrderOut(OrderBase):
    pass

@app.post('/orders', status_code=201, response_model=OrderOut)
async def create_order(order: OrderIn):
    order_dict = order.model_dump()
    order_dict.update({"order_id": "PO1001"})

    return order_dict

@app.get("/orders/{order_id}", status_code=200, response_model=OrderOut)
async def get_order(order_id: str = Path(..., regex=r'PO\d{4}')):
    order = order_data.get(order_id)
    if order:
        return order
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_id} not found.")

# alternative: best practice for professional error handler

product_data: dict = {
    'P1001': {
        "product_id": "P1001",
        "jobs": [
            "J1001"
        ],
        "quantity": 10
    }
}

class ProductBase(BaseModel):
    product_id: Optional[str] = None
    jobs: list[str]
    quantity: int

class ProductIn(ProductBase):
    role: str
    password: str

class ProductOut(ProductBase):
    pass

class ProductNotFoundException(Exception):
    def __init__(self, product_id: str):
        self.product_id = product_id


@app.get("/products/{product_id}", status_code=200, response_model=ProductOut)
async def get_product(product_id: str = Path(..., regex=r'P\d{4}')):
    product = product_data.get(product_id)
    if product:
        return product
    
    raise ProductNotFoundException(product_id)

@app.exception_handler(ProductNotFoundException)
async def product_not_found_exception_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
        'error_code': 404,
        'message': f"Product {exc.product_id} not found.",
        'info': 'additional information'
    })

# # alternative: the worst case of error handler. AVOID!!!

job_data: dict = {
    'J1001': {
        "job_id": "J1001",
        "proc_time": 60
    }
}

class JobBase(BaseModel):
    job_id: Optional[str] = None
    proc_time: int

class JobIn(JobBase):
    role: str
    password: str

class JobOut(JobBase):
    pass

class ErrorMessage(BaseModel):
    error_code: int
    message: str

@app.post('/jobs', status_code=201, response_model=JobOut, responses={
    400: {'model': ErrorMessage},
    401: {'model': ErrorMessage}
})
async def create_job(job: JobIn):
    if job_data.get(job.job_id):
        error_message = ErrorMessage(error_code=400, message=f"Job {job.job_id} already exists.")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message.model_dump())
    
    job_dict = job.model_dump()
    job_dict.update({"job_id": "J1002"})
    return job_dict


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("error_handler:app", reload=True)

