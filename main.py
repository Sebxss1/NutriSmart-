from fastapi import FastAPI

from controllers.rol_controller import router as rol_router


app = FastAPI(
    title="Nutri API",
    description="API principal de Nutri con PostgreSQL.",
    version="1.0.0",
)

app.include_router(rol_router)