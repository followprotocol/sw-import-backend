from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_v1 import api_routes
from loguru import logger
from sys import stderr
from api.config import ENV, PROJECT_NAME, DESCRIPTION

logger.remove()
logger.add(stderr, format= "<red>{level}</red>:     {message} @ <green>{time:YYYY-MM-DD | HH:mm:ss}</green>", colorize=True)
logger.add("logs/logs.log", format= "[{level}] : {message} @ {time:YYYY-MM-DD | HH:mm:ss}", rotation="50 MB")

def create_app():

    if ENV == "PROD":
        app = FastAPI(
            title=PROJECT_NAME,
            docs_url=None,
            description=DESCRIPTION,
        )
    else:
        app = FastAPI(
            title=PROJECT_NAME,
            docs_url="/",
            description=DESCRIPTION,
        )

    origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # @app.on_event("startup")
    # def on_starup():
    #     print("")

    app.include_router(api_routes)

    return app