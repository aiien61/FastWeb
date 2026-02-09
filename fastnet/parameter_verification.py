from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/orders/{order_id}")
async def get_order(order_id: str = Path(..., title="The order id", regex=r'^PO\d{3,5}$')):
    return {'order_id': order_id}

@app.get("/resources/{resource_id}")
async def get_resource(resource_id: str = Path(..., title="The resource id", min_length=5, max_length=8)):
    return {'resource_id': resource_id}

@app.get("/jobs/{job_id}")
async def get_job(job_id: str, size: int = Query(1, title="Size of Job", ge=1, le=100)):
    return {'job_id': job_id, 'size': size}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("parameter_verification:app", reload=True)
