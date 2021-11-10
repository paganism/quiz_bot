import redis
from environs import Env
import logging


log = logging.getLogger(__name__)


class Cache(redis.Redis):
    def __init__(self, host, port, password,
                 charset="utf-8",
                 decode_responses=True):
        super(Cache, self).__init__(host, port,
                                    password=password,
                                    charset=charset,
                                    decode_responses=decode_responses)
        log.info("Redis start")


env = Env()
env.read_env()

cache = Cache(
    host=env('REDIS_HOST'),
    port=env('REDIS_PORT'),
    password=env('REDIS_PASS')
)
