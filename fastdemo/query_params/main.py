from fastapi import FastAPI
from typing import Dict, Optional
import uvicorn

app = FastAPI()


@app.get("/users")
async def get_users(page_index: int, page_size: Optional[int]=30) -> Dict[str, str]:
    """
    page_index: query parameter
    page_size: query parameter
    """
    return {"users_info": f"index: {page_index}, size: {page_size}"}

@app.get("/users/{user_id}/friends")
async def get_user_friends(page_index: int, user_id: int, page_size: Optional[int]=10) -> Dict[str, str]:
    """
    page_index: query parameter
    user_id: path parameter
    page_size: query parameter
    """
    return {"user friends": f"user id: {user_id}, index: {page_index}, size: {page_size}"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)