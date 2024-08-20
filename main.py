import asyncio
import logging.config

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from infrastructure.handlers.fastapi.product import FastApiProductHandler
from infrastructure.repositories.product import SqlAlchemyProductRepository
from settings import Settings
from usecases import ProductUseCase

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "default"
        ],
        "propagate": "no"
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

settings = Settings()


async def setup() -> FastAPI:
    engine = create_async_engine(
        settings.db.get_url(),
        echo=True,
    )
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    products_repo = SqlAlchemyProductRepository(session_maker)

    products_use_case = ProductUseCase(products_repo)

    products_handler = FastApiProductHandler(products_use_case)

    app = FastAPI(
        title="Product API",
        description="API for managing products",
        version="0.1.0",
    )

    app.include_router(products_handler.router)

    return app


if __name__ == "__main__":
    app = asyncio.run(setup())
    uvicorn.run(
        app,
        host=settings.app.host,
        port=settings.app.port,
        log_config=LOGGING_CONFIG,
    )
