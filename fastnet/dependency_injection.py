from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Optional
from dataclasses import dataclass

async def set_charset():
    print('set UTF-8')

"""
Less useful: global dependency
only for certain secnarios
"""
app = FastAPI(dependencies=[Depends(set_charset)])

"""
Most useful: dependency function
"""
def pageinfo_params(page_index: Optional[int] = 1, page_size: Optional[int] = 10):
    return {"page_index": page_index, "page_size": page_size}

@app.get('/orders')
async def get_orders(page_info: dict = Depends(pageinfo_params)):
    return {"page_index": page_info.get('page_index'), "page_size": page_info.get('page_size')}

@app.get('/products')
async def get_products(page_info: dict = Depends(pageinfo_params)):
    return {"page_index": page_info.get('page_index'), "page_size": page_info.get('page_size')}

"""
Useful: dependency class
"""

@dataclass
class PageInfo:
    page_index: Optional[int] = 1
    page_size: Optional[int] = 10

@app.get('/jobs')
async def get_jobs(page_info: PageInfo = Depends(PageInfo)):
    return {"page_index": page_info.page_index, "page_size": page_info.page_size}

@app.get('/resources')
async def get_resources(page_info: PageInfo = Depends()):
    return {"page_index": page_info.page_index, "page_size": page_info.page_size}

"""
Less useful: nested dependency
"""
def total_capacity(capacity_per_hour: int) -> int:
    return capacity_per_hour * 8

def pageinfo(page_index: Optional[int] = 1, 
                    page_size: Optional[int] = 10, 
                    total_capacity: Optional[int] = Depends(total_capacity)) -> dict:
    return {"page_index": page_index, "page_size": page_size, "total_capacity": total_capacity}

@app.get('/machines')
async def get_machines(page_info: dict = Depends(pageinfo)):
    return {"page_index": page_info.get('page_index'), 
            "page_size": page_info.get('page_size'),
            "total_capacity": page_info.get('total_capacity')}

@dataclass
class PageParams:
    page_index: Optional[int] = 1
    page_size: Optional[int] = 10
    total_capacity: int = Depends(total_capacity)

@app.get('/workers')
async def get_workers(page_info: PageParams = Depends()):
    return {"page_index": page_info.page_index, 
            "page_size": page_info.page_size,
            "total_capacity": page_info.total_capacity}

"""
Most useful: multiple dependencies
"""
async def verify_auth(api_token: Optional[str] = Header(None, alias="api-token")):
    if not api_token:
        raise HTTPException(status_code=400, detail="Unauthorized")

async def connect_db(password: str = Header(None)):
    if not password:
        raise HTTPException(status_code=400, detail="Unauthorized")

@app.get('/users', dependencies=[Depends(verify_auth), Depends(connect_db)])
async def get_users(page_info: PageInfo = Depends()):
    return {"page_index": page_info.page_index, "page_size": page_info.page_size}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("dependency_injection:app", reload=True)
