from fastapi import FastAPI
from controllers import categories

app = FastAPI()

app.include_router(categories.router)

# Inicia el server: uvicorn main:app --reload
# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc