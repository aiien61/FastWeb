from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Optional
import uvicorn

async def set_charset():
    print("set UTF-8")

# Make all APIs depend on set_charset()
app = FastAPI(dependencies=[Depends(set_charset)])


async def verify_auth(api_token: Optional[str] = Header(None, alias="api-token")):
    if not api_token:
        raise HTTPException(status_code=400, detail="Unauthorized")


def total_param(total_page: Optional[int]=1):
    return total_page


def pageinfo_params(page_index: Optional[int] = 1, page_size: Optional[int] = 10, total: Optional[int]=Depends(total_param)):
    return {"page_index": page_index, "page_size": page_size, "total": total}


class PageInfo:
    def __init__(self, page_index: Optional[int] = 1, page_size: Optional[int] = 10, total: Optional[int]=Depends(total_param)):
        self.page_index = page_index
        self.page_size = page_size
        self.total = total


@app.get("/items")
async def get_items(page_info: dict=Depends(pageinfo_params)):
    return {"page_index": page_info.get("page_index"), 
            "page_size": page_info.get("page_size"),
            "total": page_info.get("total")}


@app.get("/users", dependencies=[Depends(verify_auth)])
async def get_users(page_info: dict = Depends(pageinfo_params)):
    return {"page_index": page_info.get("page_index"), "page_size": page_info.get("page_size")}


@app.get("/clients")
async def get_clients(page_info: PageInfo = Depends(PageInfo)):
    return {"page_index": page_info.page_index, "page_size": page_info.page_size}


@app.get("/products")
async def get_products(page_info: PageInfo = Depends()):
    return {"page_index": page_info.page_index, "page_size": page_info.page_size}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3_000, reload=True)