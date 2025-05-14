import logging

import uvicorn

from src.tyuiu_gpt.api.app import create_fastapi_app


app = create_fastapi_app()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app=app, host="localhost", port=8000)
