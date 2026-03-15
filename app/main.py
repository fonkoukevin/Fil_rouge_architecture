from fastapi import FastAPI
from app.presentation.auth_controller import router as auth_router
from app.presentation.manuscript_controller import router as manuscript_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(manuscript_router)