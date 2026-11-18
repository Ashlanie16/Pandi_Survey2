import hashlib
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import create_db_and_tables, engine
from models import Users, Pandi


def make_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"message": "API is running"}


@app.post("/register")
async def register(user: Users):
    with Session(engine) as session:
        taken = session.exec(select(Users).where(Users.name == user.name)).first()
        if taken:
            return {"status": "failed", "reason": "username already exists"}

        user.password = make_hash(user.password)
        session.add(user)
        session.commit()
        return {"status": "success"}


@app.post("/login")
async def login(user: Users):
    with Session(engine) as session:
        found = session.exec(
            select(Users)
            .where(Users.name == user.name)
            .where(Users.password == make_hash(user.password))
        ).first()

        if found is None:
            return {"status": "failed"}
        return {"status": "success", "name": found.name}


@app.post("/pandi")
async def save_pandi(entry: Pandi):
    with Session(engine) as session:
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return {"status": "success", "data": entry}


@app.get("/pandi")
async def list_pandi():
    with Session(engine) as session:
        return {"status": "success", "data": session.exec(select(Pandi)).all()}