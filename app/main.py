from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routes import proyectos_router, miembros_router, asignacion_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MAN_GUITO - TU AYUDANTE Y GESTOR"
    description="API para la gestión avanzada de proyectos, miembros y asignaciones.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proyectos_router.router)
app.include_router(miembros_router.router)
app.include_router(asignacion_router.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a MAN_GUITO tu gestor preferido",
        "descripcion": "Administra proyectos, miembros y asignaciones de manera profesional.",
        "documentacion": {
            "Swagger UI": "http://127.0.0.1:8000/docs",
            "ReDoc": "http://127.0.0.1:8000/redoc"
        },
        "autor": "Desarrollado por Nicolás Lozano "
    }
