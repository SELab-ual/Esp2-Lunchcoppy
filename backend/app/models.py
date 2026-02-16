from typing import Optional, List
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str
    hashed_password: str

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    phone: Optional[str] = None
    type: Optional[str] = None
    average_price: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None