from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from .db import init_db, get_session, engine
from .models import User, Restaurant
from .auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel
from .seed import seed

app = FastAPI(title="Amazing Lunch Indicator - Sprint1")

@app.on_event("startup")
def on_startup():
    init_db()
    seed()

class RegisterIn(BaseModel):
    username: str
    email: str
    password: str

class LoginIn(BaseModel):
    username: str
    password: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/register")
def register(payload: RegisterIn):
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == payload.username)).first()
        if existing:
            raise HTTPException(status_code=400, detail="username already exists")
        user = User(username=payload.username, email=payload.email, hashed_password=hash_password(payload.password))
        session.add(user)
        session.commit()
        return {"msg": "registered"}

@app.post("/login")
def login(payload: LoginIn):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == payload.username)).first()
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

from typing import Optional, List
from fastapi import Query

@app.get("/search")
def search(q: Optional[str] = None,
           min_price: Optional[int] = Query(None, ge=0),
           max_price: Optional[int] = Query(None, ge=0),
           sort_by: Optional[str] = Query("distance"),
           limit: int = Query(100, le=100)):
    with Session(engine) as session:
        stmt = select(Restaurant)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(Restaurant.name.ilike(like) | Restaurant.description.ilike(like) | Restaurant.type.ilike(like))
        if min_price is not None:
            stmt = stmt.where(Restaurant.average_price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Restaurant.average_price <= max_price)
        results = session.exec(stmt).all()
        if sort_by == "price":
            results.sort(key=lambda r: (r.average_price or 0))
        else:
            results.sort(key=lambda r: (r.id or 0))
        return {"count": len(results[:limit]), "results": [r.dict() for r in results[:limit]]}