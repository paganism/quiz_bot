import redis
from environs import Env
import logging


log = logging.getLogger(__name__)
#redis_db = redis.Redis(host='redis-19431.c250.eu-central-1-1.ec2.cloud.redislabs.com', port=19431, password='A0BzrrydytknPEFu4Su5jijSetrFB3PX', db=0)

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
