import redis

class RedisConfig(object):
    host: str
    port: int
    db: str

    def __init__(self, host: str = 'localhost', port: int = 6379):
        redis.Redis()

class RedisClient(object):
    def __init__(self):

