from datetime import date
from contextlib import asynccontextmanager
from pydantic import BaseModel, ConfigDict
from typing import List, AsyncGenerator, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy import create_engine, String, Integer, Date, select, asc, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# 1. 資料庫設定：使用 postgresql+asyncpg 驅動
# 格式: postgresql+asyncpg://user:password@host/dbname
PASSWORD: str = "database-password"
DATABASE_URL: str = f"postgresql+asyncpg://postgres:{PASSWORD}@localhost/fastapi_demo"
engine = create_async_engine(DATABASE_URL, echo=True)

# expire_on_commit = False 在非同步環境中非常重要，避免讀取已提交物件時觸發非預期的 IO
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# 2. 模型定義
class Base(DeclarativeBase):
    pass

class OrderEntity(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    due: Mapped[date] = mapped_column(Date, nullable=False) # PostgreSQL Date 對應 Python date 物件
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(128), nullable=True)

# 3. Pydantic 模型 (Schema)
class OrderBase(BaseModel):
    order_id: str
    due: date
    size: int
    description: Optional[str] = None

    # 允許從 SQLAlchemy 物件直接轉換
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: int

# 4. 資料庫依賴注入 (Dependency Injection)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 伺服器啟動時執行：自動建立所有定義在 Base 中的資料表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# --- 不涉及 IO，所以無需加入 async ---
def set_attrs(obj, data: dict):
    for key, value in data.items():
        setattr(obj, key, value)

async def get_order_by_id(order_id: str, db: AsyncSession) -> OrderEntity:
    query = select(OrderEntity).where(OrderEntity.order_id == order_id)
    result = await db.execute(query)
    existing_order = result.scalar_one_or_none()
    if not existing_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order {order_id} not found.")
    return existing_order

app = FastAPI(title="FastAPI PostgreSQL Async Demo", lifespan=lifespan)

# 5. API Endpoints
@app.get("/orders", response_model=List[OrderOut])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderEntity).order_by(asc(OrderEntity.due)))
    return result.scalars().all()

@app.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    query = select(OrderEntity).where(OrderEntity.order_id == order.order_id)
    result = await db.execute(query)
    existing_order = result.scalar_one_or_none()

    if existing_order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Order {order.order_id} already exists.")
    
    # 建立新實體
    new_order = OrderEntity(
        order_id=order.order_id,
        due=order.due,
        size=order.size,
        description=order.description
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@app.get("/orders/{order_id}", response_model=OrderOut)
async def get_order_endpoint(order_id: str = Path(...), db: AsyncSession = Depends(get_db)):
    return await get_order_by_id(order_id, db)

@app.put("/orders/{order_id}", response_model=OrderOut)
async def update_order(order_id: str = Path(...), order: OrderUpdate = ..., db: AsyncSession = Depends(get_db)):
    existing_order = await get_order_by_id(order_id, db)
    set_attrs(existing_order, order.model_dump())

    await db.commit()
    await db.refresh(existing_order)
    return existing_order

@app.delete("/orders/{order_id}")
async def delete_order(order_id: str = Path(...), db: AsyncSession = Depends(get_db)):
    existing_order = await get_order_by_id(order_id, db)
    
    await db.delete(existing_order)
    await db.flush()
    await db.commit()
    return {"message": f"Order {order_id} deleted successfully."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("database_connection:app", reload=True, host='0.0.0.0', port=8_000)
