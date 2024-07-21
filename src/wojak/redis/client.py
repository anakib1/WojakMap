from typing import Any, Dict

import redis

from ..common.config import BaseConfig
from ..common.response import Response
from ..common.codes import StatusCodes


class RedisConfig(BaseConfig):
    host: str = '127.0.0.1'
    port: int = 6379
    password: str | None
    db: int = 0


class RedisClient(object):
    """
    In future can be enhanced using custom encoding of hierarchical data.
    """

    def __init__(self, config: RedisConfig, decode_responses=True):
        self.redis = redis.Redis(host=config.host, port=config.port, db=config.db, password=config.password,
                                 decode_responses=decode_responses)

    def set(self, key: str, value: str | Dict | Any) -> Response:
        """
        Uses set for string data and hset for any other data.
        ** NOTE: IT DOES NOT UPDATE VALUES WITH THE SAME KEY, IN CONTRAST TO REGULAR CLIENT **
        :param key: key to store.
        :param value: value to store. Can be a string or anything json serializable.
        :return: None
        """
        try:
            if isinstance(value, str):
                self.redis.set(key, value)
                return Response.ok(value)
            elif isinstance(value, Dict):
                self.delete(key)
                self.redis.hset(key, mapping=value)
                return Response.ok(value)
            else:
                self.delete(key)
                self.redis.hset(key, mapping=value.__dict__)
                return Response.ok(value.__dict__)
        except Exception as ex:
            return Response(f'Unexpected redis error. Ex = {ex}', StatusCodes.REDIS_ERROR)

    def get(self, key: str) -> Response:
        """
        Gets either hierarchical, or string value.
        ASSUMPTIONS: empty dict is never a valid value and None will be returned.
        :param key:
        :return:
        """
        plain_text = None
        try:
            plain_text = self.redis.get(key)
        except redis.RedisError as ignored:
            pass
        if plain_text is not None:
            return Response.ok(plain_text)
        hierarchical = None
        try:
            hierarchical = self.redis.hgetall(key)
        except redis.RedisError as ignored:
            pass
        if len(hierarchical) == 0 or hierarchical is None:
            return Response(f'Item for key {key} was not found.', StatusCodes.ITEM_NOT_FOUND)
        return Response.ok(hierarchical)

    def delete(self, key: str) -> Response:
        """
        Returns response with deleted key.
        :param key: key to delete.
        :return: response with deleted key or ITEM_NOT_FOUND.
        """
        try:
            delete_count = self.redis.delete(key)
            if delete_count == 0:
                return Response('Could not delete item for given key. Item not found', StatusCodes.ITEM_NOT_FOUND)
            return Response.ok(key)
        except redis.RedisError as ex:
            return Response(f'Unexpected redis error. Ex = {ex}', StatusCodes.REDIS_ERROR)
