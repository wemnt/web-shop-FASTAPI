from fastapi import FastAPI

from api.errors import register_exception_handlers
from api.v1.router import api_router

app = FastAPI()
register_exception_handlers(app)
app.include_router(api_router)
