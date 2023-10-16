from fastapi import FastAPI

from api.config import settings
from api.errors import error_handler

app = FastAPI(title=settings.PROJECT_NAME)

error_handler(app)


@app.get('/')
async def _():
    return {'msg': 'hello world'}
