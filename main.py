from sqlmodel import SQLModel
from app.memory.db import engine
from contextlib import asynccontextmanager
from fastapi import FastAPI,HTTPException,Depends
from app.memory.models import Contact,Memory,Goal
from app.orchestrator.coo import COOAgent
from pydantic import BaseModel
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

    
app:FastAPI=FastAPI(lifespan=lifespan)
coo = COOAgent()

class Request(BaseModel):
      query:str
      
      
@app.post("/ask")
def ai_ask(req:Request):
    result = coo.process(req.query)
    return {
            "query" : req.query,
            "result" : result
        }
        
        
        
        