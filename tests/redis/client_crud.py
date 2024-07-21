import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from wojak.common.codes import StatusCodes
from wojak.redis.client import RedisClient, RedisConfig


class RedisNaiveOperations(unittest.TestCase):
    def setUp(self):
        self.client = RedisClient(RedisConfig())
        self.key = 'foo'

        self.client.delete(self.key)
        self.client.delete(self.key)

    def verify_crud(self, key, value1, value2):
        self.assertEqual(self.client.get(key).status, StatusCodes.ITEM_NOT_FOUND)
        self.assertTrue(self.client.set(key, value1).is_ok())
        self.assertEqual(self.client.get(key).content, value1)
        self.assertTrue(self.client.set(key, value2).is_ok())
        self.assertEqual(self.client.get(key).content, value2)
        self.assertTrue(self.client.delete(key).is_ok())
        self.assertEqual(self.client.get(key).status, StatusCodes.ITEM_NOT_FOUND)

    def test_crud_str(self):
        self.verify_crud(self.key, 'bar', 'gar')

    def test_crud_dict(self):
        self.verify_crud(self.key, {'hard': 'bar'}, {'easy': 'bar'})


if __name__ == '__main__':
    unittest.main()
