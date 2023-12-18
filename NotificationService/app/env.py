from aiokafka import AIOKafkaProducer, AIOKafkaConsumer  # AIOKafkaClient
import asyncio

from .config import settings
from .consumers import cons1

loop = asyncio.get_event_loop()
aioproducers = [AIOKafkaProducer(loop=loop, bootstrap_servers=settings.KAFKA_INSTANCE)]
consumers = [{"consumer": AIOKafkaConsumer("cons1", bootstrap_servers=settings.KAFKA_INSTANCE, loop=loop),
              "consume": cons1.consume}]