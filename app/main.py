from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.route import app as api_router

app = FastAPI(
    title="Object Detection API",
    description="A simple API that detects objects in an image for an interview",
    version="0.1.0",
    docs_url="/documentation",
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)
