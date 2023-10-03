import asyncio
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.api_v1.api import api_router
from src.core.config import app_configs, settings
from src.database.postgres.database import init_tables
from src.kafka.consumer import consume as kafka_consume
from src.kafka.consumer import consumer as kafka_consumer
from src.kafka.consumer import initialize as kafka_initialize
from src.kafka.producer import producer as kafka_producer

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
log = logging.getLogger(__name__)

app = FastAPI(**app_configs)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():
    log.info("Initializing API ...")
    asyncio.create_task(init_tables())
    # await kafka_producer.start()
    # await kafka_initialize()
    # await kafka_consume()


# @app.on_event("shutdown")
# async def shutdown():
#     await kafka_producer.stop()
#     await kafka_consumer.stop()
