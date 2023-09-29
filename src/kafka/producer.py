import json

from aiokafka import AIOKafkaProducer

from src.core.config import settings

producer = AIOKafkaProducer(
    bootstrap_servers=[
        f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
    ],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)
