import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from wojak.http.client import RequestBuilder
from wojak.common.codes import StatusCodes


class RequestBuilderTest(unittest.TestCase):
    def test_status_ok(self):
        self.assertTrue(RequestBuilder('https://api.github.com/').append_url('/events').get().json().is_ok())

    def test_post_ok(self):
        self.assertTrue(
            RequestBuilder('https://httpbin.org/')
            .append_url('post')
            .json({'a': 'b', 'c': 'd'})
            .post()
            .json()
            .is_ok())

    def test_post_content(self):
        self.assertEqual(
            RequestBuilder('https://httpbin.org/')
            .append_url('post')
            .json({'a': 'b', 'c': 'd'})
            .post()
            .json().content,
        {'a': 'b', 'c': 'd'})

    def test_wrong_type(self):
        self.assertEqual(
            RequestBuilder('https://httpbin.org/')
            .append_url('post')
            .json({'a': 'b', 'c': 'd'})
            .get()
            .json().status, StatusCodes.HTTP_ERROR + 405)


if __name__ == '__main__':
    unittest.main()
