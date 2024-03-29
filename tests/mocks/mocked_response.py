import json

from httpx import Response


class MockedResponse(Response):
    """Mocked response for testing"""

    def __init__(self, *args, **kwargs) -> None:
        """class initialization"""
        self.status_code = kwargs.get("status_code")
        self.reason = kwargs.get("reason", "")
        self.encoding = "UTF-8"
        self._content = str.encode(json.dumps({}))
        super().__init__(self.status_code)
