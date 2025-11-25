import os

class Config:
    # clave para sesiones y CSRF (no poner esto en producción asi)
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-super-secreta-para-tp")

    # config de base de datos MySQL (Clever Cloud o local)
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
    DB_NAME = os.environ.get("DB_NAME", "portafolio_matias")
