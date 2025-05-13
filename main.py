import logging

import uvicorn

from src.tyuiu_gpt.api.app import create_fastapi_app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = create_fastapi_app()
    uvicorn.run(app=app, host="localhost", port=8000)
