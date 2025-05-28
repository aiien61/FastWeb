from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
