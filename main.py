import time
from ipaddress import ip_address
from typing import Callable

import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from src.database.db import get_db
from src.routes import contacts, auth, users
from src.conf.config import settings


app = FastAPI()


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    await FastAPILimiter.init(r)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ALLOWED_IPS = [
    ip_address("192.168.1.0"),
    ip_address("172.16.0.0"),
    ip_address("127.0.0.1"),
]


@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip not in ALLOWED_IPS:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not allowed IP address"},
        )
    response = await call_next(request)
    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response


@app.get("/")
def read_root():
    return {"message": "REST APP v1.2"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")
