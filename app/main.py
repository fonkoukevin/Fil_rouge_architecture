from fastapi import FastAPI
from app.presentation.auth_controller import router as auth_router
from app.presentation.manuscript_controller import router as manuscript_router
from app.presentation.editorial_controller import router as editorial_router
from app.presentation.publication_controller import router as publication_router
from app.presentation.notification_controller import router as notification_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(manuscript_router)
app.include_router(editorial_router)
app.include_router(publication_router)
app.include_router(notification_router)
