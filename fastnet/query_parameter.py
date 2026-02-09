from fastapi import FastAPI
from typing import Optional
from datetime import datetime

app = FastAPI()

@app.get("/orders")
async def get_orders(month: int, year: Optional[int] = datetime.now().year):
    return {"year": year, "month": month}

@app.get("/{order_id}/jobs")
async def get_orders(year: int, order_id: str, month: int):
    return {"year": year, "month": month, "order_id": order_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("query_parameter:app", reload=True)