import asyncio
from fastapi import FastAPI
from utils import rounter
from database import database



app = FastAPI()



@app.get("/")
async def hello_message():
    return {"message":"all working"}

app.include_router(rounter)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()