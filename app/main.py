from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.mongodb import(connect_to_mongodb)

from app.routes.meetings import router

app = FastAPI(title = settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongodb()

app.include_router(router)

app.get("/")
async def root():
    return {"message": "Hello World"}
