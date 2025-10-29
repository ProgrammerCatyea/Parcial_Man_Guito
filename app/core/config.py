"""Configuración general del sistema y variables de entorno."""


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Parcial_Man_Guito – Gestor de Proyectos"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./parcial_manguito.db"

    class Config:
        env_file = ".env"

settings = Settings()
