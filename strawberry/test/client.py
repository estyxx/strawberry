from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

from typing_extensions import Literal, TypedDict


@dataclass
class Response:
    errors: Optional[Dict[str, Any]]
    data: Optional[Dict[str, Any]]
    extensions: Optional[Dict[str, Any]]


class Body(TypedDict, total=False):
    query: str
    variables: Optional[Dict[str, Any]]


class BaseGraphQLTestClient(ABC):
    def __init__(self, client):
        self._client = client

    @abstractmethod
    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        asserts_errors: Optional[bool] = True,
        format: Literal["multipart", "json"] = "json",
        files: Optional[Dict[str, Any]] = None,
    ) -> Response:
        raise NotImplementedError
