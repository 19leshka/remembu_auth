import asyncio
import json
import logging
from random import randint
from typing import Any, Set

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import TopicPartition

from src.core.config import settings

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# global variables
consumer_task = None
consumer = None
_state = 0


async def initialize():
    loop = asyncio.get_event_loop()
    global consumer
    group_id = f"{settings.KAFKA_CONSUMER_GROUP_PREFIX}-{randint(0, 10000)}"
    logger.debug(
        f"Initializing KafkaConsumer for topic {settings.KAFKA_TOPIC}, group_id {group_id}"
        f" and using bootstrap servers {settings.KAFKA_HOST}:{settings.KAFKA_PORT}"
    )
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        loop=loop,
        bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
        group_id=group_id,
    )
    # get cluster layout and join group
    await consumer.start()

    partitions: Set[TopicPartition] = consumer.assignment()
    nr_partitions = len(partitions)
    if nr_partitions != 1:
        logger.warning(
            f"Found {nr_partitions} partitions for topic {settings.KAFKA_TOPIC}. Expecting "
            f"only one, remaining partitions will be ignored!"
        )
    for tp in partitions:
        # get the log_end_offset
        end_offset_dict = await consumer.end_offsets([tp])
        end_offset = end_offset_dict[tp]

        if end_offset == 0:
            logger.warning(
                f"Topic ({settings.KAFKA_TOPIC}) has no messages (log_end_offset: "
                f"{end_offset}), skipping initialization ..."
            )
            return

        logger.debug(f"Found log_end_offset: {end_offset} seeking to {end_offset-1}")
        consumer.seek(tp, end_offset - 1)
        msg = await consumer.getone()
        logger.info(f"Initializing API with data from msg: {msg}")

        # update the API state
        _update_state(msg)
        return


def _update_state(message: Any) -> None:
    value = json.loads(message.value)
    global _state
    _state = value


async def send_consumer_message(consumer: AIOKafkaConsumer):
    try:
        # consume messages
        async for msg in consumer:
            logger.info(f"Consumed msg: {msg}")
            _update_state(msg)
    finally:
        logger.warning("Stopping consumer")
        await consumer.stop()


async def consume():
    global consumer_task
    consumer_task = asyncio.create_task(send_consumer_message(consumer))
