from typing import Any
from .codes import StatusCodes


class Response:
    """
    Response class. Confirms with the following facts:
        status = 2xx -> content != None & comment = None

        status != 2xx -> content = None & comment != None

    """
    comment: str
    status: int
    content: Any

    def __init__(self, comment: str | None, status: int, content: Any = None):
        self.comment = comment
        self.status = status
        self.content = content

    def __repr__(self):
        return f'Response(comment={self.comment}, status={self.status}, content={self.content}))'

    def is_ok(self) -> bool:
        return self.status == StatusCodes.OK

    @classmethod
    def ok(cls, content):
        return cls(None, StatusCodes.OK, content)
