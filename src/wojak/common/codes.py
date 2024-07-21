class StatusCodes:
    """
    Status codes enumeration for Response<> class.
    """
    OK = 200
    TIMEOUT = 408
    INTERNAL_SERVICE_ERROR = 500
    ITEM_NOT_FOUND = 601
    REDIS_ERROR = 602
    JSON_CONVERSION_ERROR = 603
    HTTP_ERROR = 10000  # Comment contains HTTP description.


