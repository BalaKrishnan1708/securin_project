from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.cpes import router as cpe_router

def create_app():
    app = FastAPI(title="CPE Search API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(cpe_router)
    
    return app

app = create_app()
