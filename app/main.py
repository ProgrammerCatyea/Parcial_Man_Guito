from fastapi import FastAPI
from .core.config import settings
from .core.database import Base, engine
from .routes import proyectos_router, miembros_router, asignaciones_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="API para gestión de proyectos con miembros, gerente y asignaciones.",
    version="1.0.0",
)

app.include_router(miembros_router.router)
app.include_router(proyectos_router.router)
app.include_router(asignaciones_router.router)

@app.get("/", tags=["Inicio"])
def root():
    return {"mensaje": "Bienvenido a Man_Guito tu gestor de proyectos preferido!"}
