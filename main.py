from fastapi import FastAPI
from routes.route import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(router)