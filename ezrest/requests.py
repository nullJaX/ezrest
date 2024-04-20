from typing import Any, AsyncIterator, Generic, Iterator, TypeVar, Union
from urllib.parse import urlparse, urlunparse

# Represents the type of the REST API response
# In most cases it will be a JSON response (ie. Dict[str, Any])
_ResponseType = TypeVar("_ResponseType")


class Connector(Generic[_ResponseType]):
    """
    Synchronous Connector - defines general behavior for interacting with
    specific REST API.

    This 'interface' class contains all HTTP methods that are commonly used in
    REST APIs. The methods themselves (POST, GET, PUT, PATCH, DELETE) are not
    implemented so that developers can pick HTTP library of choice.
    Each method accepts URL as a first argument, the rest of the arguments
    (such as URL headers or parameters) are up to developer's discretion.

    There is also one additional method, list(), its purpose is to provide
    iterator-like behavior for the endpoints returning collections and/or
    to handle paginated responses. The `list` method should handle these
    responses and always `yield` items/resources one-by-one.

    NOTE: To keep your code simple and maintainable, the implementations of
    this class should not define how the resources are converted from and into
    objects/dataclasses. The intended scope of a connector is to provide
    unified interface between client and a server on a request-response level,
    possibly with authentication scheme and error handling.
    """

    def post(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP POST request"""
        raise NotImplementedError()

    def get(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP GET request"""
        raise NotImplementedError()

    def put(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP PUT request"""
        raise NotImplementedError()

    def patch(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP PATCH request"""
        raise NotImplementedError()

    def delete(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP DELETE request"""
        raise NotImplementedError()

    def list(self, url: str, *args, **kwargs) -> Iterator[_ResponseType]:
        """
        Returns items/resources one-by-one for endpoints returning collections
        and/or paginated responses.

        Example:

        def list(self, url: str, *args, **kwargs) -> Iterator[ResponseType]:
            next_url: str = url
            while next_url:
                response = self.get(url, *args, **kwargs).json()
                for item in response.get("items", []):
                    yield item
                next_url = response.get("next")
        """
        raise NotImplementedError()


class AsyncConnector(Generic[_ResponseType]):
    """
    Asynchronous Connector - defines general behavior for interacting with
    specific REST API.

    This 'interface' class contains all HTTP methods that are commonly used in
    REST APIs. The methods themselves (POST, GET, PUT, PATCH, DELETE) are not
    implemented so that developers can pick HTTP library of choice.
    Each method accepts URL as a first argument, the rest of the arguments
    (such as URL headers or parameters) are up to developer's discretion.

    There is also one additional method, list(), its purpose is to provide
    iterator-like behavior for the endpoints returning collections and/or
    to handle paginated responses. The `list` method should handle these
    responses and always `yield` items/resources one-by-one.

    NOTE: To keep your code simple and maintainable, the implementations of
    this class should not define how the resources are converted from and into
    objects/dataclasses. The intended scope of a connector is to provide
    unified interface between client and a server on a request-response level,
    possibly with authentication scheme and error handling.
    """

    async def post(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP POST request"""
        raise NotImplementedError()

    async def get(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP GET request"""
        raise NotImplementedError()

    async def put(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP PUT request"""
        raise NotImplementedError()

    async def patch(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP PATCH request"""
        raise NotImplementedError()

    async def delete(self, url: str, *args, **kwargs) -> _ResponseType:
        """Performs HTTP DELETE request"""
        raise NotImplementedError()

    async def list(self, url: str, *args, **kwargs) -> AsyncIterator[_ResponseType]:
        """
        Returns items/resources one-by-one for endpoints returning collections
        and/or paginated responses.

        Example:

        async def list(self, url: str, *args, **kwargs) -> AsyncIterator[ResponseType]:
            next_url: str = url
            while next_url:
                response = await self.get(url, *args, **kwargs).json()
                for item in response.get("items", []):
                    yield item
                next_url = response.get("next")
        """
        raise NotImplementedError()
        yield None  # pragma: no cover # supresses mypy error


# Types that unify synchronous and asynchronous connector usage in
# BaseEndpoint class.
_ConnectorType = TypeVar("_ConnectorType", bound=Union[AsyncConnector, Connector])


class BaseEndpoint(Generic[_ConnectorType, _ResponseType]):
    """
    (Async)Endpoint [Builder]

    This class allows for generating endpoint URLs dynamically without
    hardcoding endpoint suffixes and uses (Async)Connector instance to
    perform requests.

    The (Async)Endpoint usage is explained in the following snippet.
    There is no significant difference between synchronous and asynchronous
    version other than the class names used. Each example will generate a
    copy of the (Async)Endpoint with modified URL, but the (Async)Connector
    instance will be shared with the newly created (Async)Endpoint. On each
    (Async)Endpoint one can call methods implemented in the (Async)Connector.
    Note, however, that these methods don't accept URL as the first argument,
    it is automatically injected. The rest of the arguments are passed through
    without any modifications.

    Examples:

    base_url = 'http://x.com/'

    connector = Connector[Dict[str, Any]] ()

    api_root = Endpoint[Dict[str, Any]](base_url, connector)

    api_root                # http://x.com/
    api_root.posts          # http://x.com/posts
    api_root.comments[3]    # http://x.com/comments/3
    api_root["comments"][3] # http://x.com/comments/3

    api_root.comments.3     # Not allowed, 3 is not a string type
    """

    url: str
    """URL of the current endpoint"""

    connector: _ConnectorType
    """Connector instance that is used to perform requests"""

    def __init__(self, url: str, connector: _ConnectorType) -> None:
        self.url = self._sanitize_url(url)
        self.connector = connector

    @staticmethod
    def _sanitize_url(url: str) -> str:
        """
        Sanitizes the URL
        (removes parameters, queries, fragments and excessive trailing slashes)
        """
        parsed_url = urlparse(url)
        path = parsed_url.path
        while path.endswith("/"):
            path = path[:-1]
        return urlunparse(
            parsed_url._replace(path=path, params="", query="", fragment="")
        )

    def _generate_endpoint(self, name: Any):
        """
        Creates new endpoint object (for subresources) with:
        - the same type as the parent endpoint object
        - the same instance of the connector
        - name of the resource appended at the end of the URL
        """
        return type(self)(self._get_sub_resource_url(name), self.connector)

    def _get_sub_resource_url(self, name: Any) -> str:
        """
        Generates new URL with the name of the resource appended at the end
        """
        return f"{self.url}/{str(name)}"

    __getattr__ = __getitem__ = _generate_endpoint

    def post(self, *args, **kwargs):
        """Executes HTTP POST request via connector"""
        return self.connector.post(self.url, *args, **kwargs)

    def get(self, *args, **kwargs):
        """Executes HTTP GET request via connector"""
        return self.connector.get(self.url, *args, **kwargs)

    def put(self, *args, **kwargs):
        """Executes HTTP PUT request via connector"""
        return self.connector.put(self.url, *args, **kwargs)

    def patch(self, *args, **kwargs):
        """Executes HTTP PATCH request via connector"""
        return self.connector.patch(self.url, *args, **kwargs)

    def delete(self, *args, **kwargs):
        """Executes HTTP DELETE request via connector"""
        return self.connector.delete(self.url, *args, **kwargs)

    def list(self, *args, **kwargs):
        """Runs connector's list method to retrieve items one-by-one"""
        return self.connector.list(self.url, *args, **kwargs)


# Type aliases that are more convenient to use.
# If the response type is Dict[str, Any],
# instantiation will look like this:
#
# endpoint = endpoint = Endpoint[Dict[str, Any]](url, Connector())
# async_endpoint = AsyncEndpoint[Dict[str, Any]](url, AsyncConnector())
#
# and inheritance will look like this:
#
# class MyEndpoint(Endpoint[Dict[str, Any]]):
#     ...
# class MyAsyncEndpoint(AsyncEndpoint[Dict[str, Any]]):
#     ...
#
Endpoint = BaseEndpoint[Connector[_ResponseType], _ResponseType]
AsyncEndpoint = BaseEndpoint[AsyncConnector[_ResponseType], _ResponseType]
