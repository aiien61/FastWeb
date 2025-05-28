from fastapi import FastAPI, HTTPException, Depends, Path
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
import uvicorn

from models import User, UserUpdate
from db_session import get_session
from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/users/")
async def create_user(user: User, session: AsyncSession = Depends(get_session)):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@app.get("/users/")
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User))
    return result.scalars().all()

@app.patch("/users/{user_id}")
async def update_user(*, user_id: int, user_update: UserUpdate, 
                      session: AsyncSession = Depends(get_session)):
    
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User (id={user_id}) not found")
    
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
async def delete_user(*, user_id: int, session: AsyncSession = Depends(get_session)):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await session.delete(db_user)
    await session.commit()
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3_000, reload=True)
