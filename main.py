import logging

from src.api.app import create_fastapi_app


logging.basicConfig(level=logging.INFO)

app = create_fastapi_app()
