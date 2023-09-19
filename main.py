import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from controllers import categories, socialsources, youtube

load_dotenv()

api_port = os.environ.get("API_PORT")

app = FastAPI()


origins = [
    "http://localhost:3002",  # TODO change to allow only requests from ApiGateway
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(categories.router)
app.include_router(socialsources.router)
app.include_router(youtube.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=api_port)

# Inicia el server: uvicorn main:app --reload
# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
