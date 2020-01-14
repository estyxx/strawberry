import json
import logging
from typing import Optional

import pytest

from django.test.client import RequestFactory

import strawberry
from strawberry.django.views import GraphQLView as BaseGraphQLView
from strawberry.permission import BasePermission

from .app.models import Example


class AlwaysFailPermission(BasePermission):
    message = "You are not authorized"

    def has_permission(self, source, info):
        return False


@strawberry.type
class Query:
    hello: str = "strawberry"

    @strawberry.field
    async def hello_async(self, info) -> str:
        return "async strawberry"

    @strawberry.field(permission_classes=[AlwaysFailPermission])
    def always_fail(self, info) -> Optional[str]:
        return "Hey"

    @strawberry.field
    async def example_async(self, info) -> str:
        return Example.objects.first().name

    @strawberry.field
    def example(self, info) -> str:
        return Example.objects.first().name


schema = strawberry.Schema(query=Query)


class GraphQLView(BaseGraphQLView):
    def get_root_value(self):
        return Query()


def test_playground_view():
    factory = RequestFactory()

    request = factory.get("/graphql/", HTTP_ACCEPT="text/html")

    response = GraphQLView.as_view(schema=schema)(request)
    body = response.content.decode()

    assert "GraphQL Playground" in body
    assert f'endpoint: "{request.get_full_path()}"' in body


def test_graphql_query():
    query = "{ hello }"

    factory = RequestFactory()
    request = factory.post(
        "/graphql/", {"query": query}, content_type="application/json"
    )

    response = GraphQLView.as_view(schema=schema)(request)
    data = json.loads(response.content.decode())

    assert data["data"]["hello"] == "strawberry"


@pytest.mark.django_db
def test_graphql_query_model():
    Example.objects.create(name="This is a demo")

    query = "{ example }"

    factory = RequestFactory()
    request = factory.post(
        "/graphql/", {"query": query}, content_type="application/json"
    )

    response = GraphQLView.as_view(schema=schema)(request)
    data = json.loads(response.content.decode())

    assert data["data"]["example"] == "This is a demo"


@pytest.mark.xfail(reason="We don't support async on django at the moment")
def test_async_graphql_query():
    query = "{ helloAsync }"

    factory = RequestFactory()
    request = factory.post(
        "/graphql/", {"query": query}, content_type="application/json"
    )

    response = GraphQLView.as_view(schema=schema)(request)
    data = json.loads(response.content.decode())

    assert data["data"]["helloAsync"] == "async strawberry"


@pytest.mark.xfail(reason="We don't support async on django at the moment")
def test_async_graphql_query_model():
    Example.objects.create(name="This is a demo async")

    query = "{ exampleAsync }"

    factory = RequestFactory()
    request = factory.post(
        "/graphql/", {"query": query}, content_type="application/json"
    )

    response = GraphQLView.as_view(schema=schema)(request)
    data = json.loads(response.content.decode())

    assert data["data"]["exampleAsync"] == "This is a demo async"


def test_returns_errors_and_data():
    query = "{ hello, alwaysFail }"

    factory = RequestFactory()
    request = factory.post(
        "/graphql/", {"query": query}, content_type="application/json"
    )

    response = GraphQLView.as_view(schema=schema)(request)
    data = json.loads(response.content.decode())

    assert response.status_code == 200

    assert data["data"]["hello"] == "strawberry"
    assert data["data"]["alwaysFail"] is None


class ListHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super(ListHandler, self).__init__(*args, **kwargs)

        for level in logging._nameToLevel.keys():
            setattr(self, level.lower(), [])

    def emit(self, record):
        msg = record.getMessage()
        getattr(self, record.levelname.lower()).append(msg)


@pytest.fixture
def get_logger():
    logger = logging.getLogger("test")
    logger.setLevel(logging.WARNING)

    handler = ListHandler()
    logger.addHandler(handler)

    return logger, handler


def test_log_handled_error(get_logger):
    logger, handler = get_logger

    query = "{ hello, alwaysFail }"

    factory = RequestFactory()
    request = factory.post(
        "/graphql/", {"query": query}, content_type="application/json"
    )
    GraphQLView.as_view(schema=schema, logger=logger)(request)
    assert handler.error == ["You are not authorized"]


def test_log_unhandled_error(get_logger):
    logger, handler = get_logger

    query = "{ hello, mistake }"

    factory = RequestFactory()
    request = factory.post(
        "/graphql/", {"query": query}, content_type="application/json"
    )

    GraphQLView.as_view(schema=schema, logger=logger)(request)
    assert handler.error == [
        "Cannot query field 'mistake' on type 'Query'.\n\nGraphQL request:1:10\n1 | { hello, mistake }\n  |          ^"  # noqa
    ]
