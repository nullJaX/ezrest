from typing import AsyncIterator, Generic, Iterator, TypeVar

# Generic type that indicates the resource type.
# It can be a dataclass, a NamedTuple or just a class holding data
# reflecting server resource state.
_ResourceType = TypeVar("_ResourceType")


class CRUD(Generic[_ResourceType]):
    """
    CRUD interface - defines the server data access on the object level.

    This class serves as an interface for mapping between REST API responses
    and a container object holding the server data state, as well as providing
    read and modification functions following the CRUD principle.

    The actual body of CRUD methods (CREATE, READ, UPDATE, DELETE) is intentionally
    left unimplemented due to the varying schema and interaction requirements
    across specific REST APIs. All modification methods accept an instance of
    the resource and should return the latest server state of the resource after
    performing the operation (the DELETE method should still return the resource
    containing data before deletion).

    There is also one additional method, list(), designed to offer iterator-like
    behavior for endpoints returning collections and/or handling paginated responses.
    The list() method handles these responses and iteratively `yields` resources
    one-by-one.

    NOTE: To ensure simplicity and maintainability of your code, implementations
    of the CRUD class should focus on defining interaction at the object level,
    optionally incorporating parsing and unparsing mechanisms. Network/HTTP
    interaction should be delegated to a separate component or layer.
    """

    def create(self, resource: _ResourceType, *args, **kwargs) -> _ResourceType:
        """
        Creates a new resource on the server.
        Returns the latest resource state (including any keys/ids).
        """
        raise NotImplementedError()

    def update(self, resource: _ResourceType, *args, **kwargs) -> _ResourceType:
        """
        Updates an existing resource on the server.
        Returns the latest resource state (including any keys/ids).
        """
        raise NotImplementedError()

    def delete(self, resource: _ResourceType, *args, **kwargs) -> _ResourceType:
        """
        Deletes an existing resource on the server.
        Returns the same resource instance.
        """
        raise NotImplementedError()

    def read(self, *args, **kwargs) -> _ResourceType:
        """Reads a single resource from the server."""
        raise NotImplementedError()

    def list(self, *args, **kwargs) -> Iterator[_ResourceType]:
        """
        Yields resources one-by-one for endpoints returning collections
        and/or paginated responses.
        """
        raise NotImplementedError()


class AsyncCRUD(Generic[_ResourceType]):
    """
    AsyncCRUD interface - defines the server data access on the object level.

    This class serves as an interface for mapping between REST API responses
    and a container object holding the server data state, as well as providing
    read and modification functions following the CRUD principle.

    The actual body of CRUD methods (CREATE, READ, UPDATE, DELETE) is intentionally
    left unimplemented due to the varying schema and interaction requirements
    across specific REST APIs. All modification methods accept an instance of
    the resource and should return the latest server state of the resource after
    performing the operation (the DELETE method should still return the resource
    containing data before deletion).

    There is also one additional method, list(), designed to offer iterator-like
    behavior for endpoints returning collections and/or handling paginated responses.
    The list() method handles these responses and iteratively `yields` resources
    one-by-one.

    NOTE: To ensure simplicity and maintainability of your code, implementations
    of the CRUD class should focus on defining interaction at the object level,
    optionally incorporating parsing and unparsing mechanisms. Network/HTTP
    interaction should be delegated to a separate component or layer.
    """

    async def create(self, resource: _ResourceType, *args, **kwargs) -> _ResourceType:
        """
        Creates a new resource on the server.
        Returns the latest resource state (including any keys/ids).
        """
        raise NotImplementedError()

    async def update(self, resource: _ResourceType, *args, **kwargs) -> _ResourceType:
        """
        Updates an existing resource on the server.
        Returns the latest resource state (including any keys/ids).
        """
        raise NotImplementedError()

    async def delete(self, resource: _ResourceType, *args, **kwargs) -> _ResourceType:
        """
        Deletes an existing resource on the server.
        Returns the same resource instance.
        """
        raise NotImplementedError()

    async def read(self, *args, **kwargs) -> _ResourceType:
        """Reads a single resource from the server."""
        raise NotImplementedError()

    async def list(self, *args, **kwargs) -> AsyncIterator[_ResourceType]:
        """
        Yields resources one-by-one for endpoints returning collections
        and/or paginated responses.
        """
        raise NotImplementedError()
        yield None  # pragma: no cover # supresses mypy error
