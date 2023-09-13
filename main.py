import uvicorn
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from controllers import categories

load_dotenv()

api_port = os.environ.get("API_PORT")

app = FastAPI()

app.include_router(categories.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=api_port)

# Inicia el server: uvicorn main:app --reload
# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc