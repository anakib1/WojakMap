import json
from typing import Any

import requests

from ..common.codes import StatusCodes
from ..common.response import Response


class HttpResponse(Response):
    def json(self):
        if not self.is_ok():
            return self
        try:
            return Response.ok(json.loads(self.content)['json'])
        except Exception as ex:
            return Response(f'Failed to convert output to json. Ex = {ex}', StatusCodes.JSON_CONVERSION_ERROR)


class RequestBuilder:
    """
    Builder-style wrapper around python requests library. View other methods documentation for detailed
    class introduction.

    This request wrapped does not raise explicit exception and incorporates exceptions into response format.
    """

    def __init__(self, base_url: str = '', timeout_ms: int = 1000):
        """
        Created builder with basic url.
        :param timeout_ms: timeout for request.
        :param base_url: url of the request. Example: http://127.0.0.1:8011/api/v1.
        """
        self.timeout = timeout_ms
        self.request_url = base_url
        self.params = {}
        self.headers = {}
        self.data = None
        self.response = None

    def append_url(self, url: str) -> 'RequestBuilder':
        """
        Appends request URL with provided argument.
        :param url: Suffix to append to request URL.
        :return: Updated request builder instance.
        """
        if self.request_url.endswith('/') and url.startswith('/'):
            url = url[1:]
        self.request_url = self.request_url + url
        return self

    def header(self, header_key, header_value) -> 'RequestBuilder':
        """
        Adds new request header. In case of multiple headers sharing the same key will be added as list
        to corresponding key entry.
        :param header_key: header key to add.
        :param header_value: header value to add.
        :return: Updated request builder instance.
        """
        if header_key in self.headers:
            self.headers[header_key] = [self.headers[header_key], header_value]
        else:
            self.headers[header_key] = header_value
        return self

    def param(self, param_name: str, param_value: Any) -> 'RequestBuilder':
        """
        Adds new request param. In case of multiple params sharing the same key will be added as list
        to corresponding key entry. This behavior is described at requests documentation.
        :param param_name: param key to add.
        :param param_value: param value to add.
        :return: Updated request builder instance.
        """
        if param_name in self.params:
            self.params[param_name] = [self.params[param_name], param_value]
        else:
            self.params[param_name] = param_value
        return self

    def data(self, data: str) -> 'RequestBuilder':
        """
        Sets request data to provided argument in string format.
        :param data: data to incorporate in request;
        :return: Updated request builder instance.
        """
        self.data = data
        return self

    def json(self, data: Any) -> 'RequestBuilder':
        """
        Sets request data to json dump of provided argument.
        :param data: any json-serialize object to provide request data.
        :return: Updated request builder instance.
        """
        self.data = json.dumps(data)
        return self

    def _wrap_requests_exception(self, exception: Exception) -> HttpResponse:
        if isinstance(exception, requests.RequestException):
            if isinstance(exception, requests.exceptions.Timeout):
                return HttpResponse(f'Request timed out. Wait time = {self.timeout}ms', StatusCodes.TIMEOUT, None)
            elif isinstance(exception, requests.exceptions.ConnectionError):
                return HttpResponse('Connection error.', StatusCodes.INTERNAL_SERVICE_ERROR, None)
            else:
                return HttpResponse(f'Unexpected exception occurred on requests side. Ex = {exception}',
                                    StatusCodes.INTERNAL_SERVICE_ERROR, None)
        raise exception

    def _wrap_response(self, response: requests.Response) -> HttpResponse:
        if response.ok:
            return HttpResponse(None, StatusCodes.OK, response.content)
        return HttpResponse(f'Unexpected status code {response.status_code}. Reason = {response.reason}',
                            StatusCodes.HTTP_ERROR + response.status_code,
                            None)

    def get(self) -> HttpResponse:
        """
        Gets with given parameters headers and data.
        :return: Response instance.
        """
        try:
            request_response = requests.get(url=self.request_url,
                                            params=self.params,
                                            headers=self.headers,
                                            data=self.data,
                                            timeout=self.timeout)
            return self._wrap_response(request_response)
        except Exception as ex:
            return self._wrap_requests_exception(ex)

    def post(self) -> HttpResponse:
        """
        Posts with given parameters headers and data.
        :return: Response instance.
        """
        try:
            request_response = requests.post(url=self.request_url,
                                             params=self.params,
                                             headers=self.headers,
                                             data=self.data,
                                             timeout=self.timeout)
            return self._wrap_response(request_response)
        except Exception as ex:
            return self._wrap_requests_exception(ex)
