from typing import Any, AsyncIterator, Dict, Iterator, NamedTuple, Optional
from httpx import AsyncClient, Client
from ezrest.objects import AsyncCRUD, CRUD
from ezrest.requests import AsyncConnector, AsyncEndpoint, Connector, Endpoint

JSONType = Dict[str, Any]
OptionalJSONType = Optional[JSONType]

# The service used in the tests is documented here:
# https://reqres.in/
BASE_URL = "https://reqres.in/api"


class ReqResConnector(Connector[JSONType]):
    client: Client

    def __init__(self) -> None:
        self.client = Client()

    def _data_request(
        self, method: str, url: str, data: OptionalJSONType = None
    ) -> JSONType:
        response = getattr(self.client, method)(url, data=data)
        response.raise_for_status()
        return response.json()

    def post(self, url: str, data: OptionalJSONType = None) -> JSONType:
        return self._data_request("post", url, data=data)

    def put(self, url: str, data: OptionalJSONType = None) -> JSONType:
        return self._data_request("put", url, data=data)

    def patch(self, url: str, data: OptionalJSONType = None) -> JSONType:
        return self._data_request("patch", url, data=data)

    def delete(self, url: str) -> JSONType:
        response = self.client.delete(url)
        response.raise_for_status()
        return {"code": response.status_code}

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> JSONType:
        params = params or {}
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def list(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Iterator[JSONType]:
        params = params or {}
        page: int = int(params.get("page", 0))
        total_pages: int = page + 1
        while page < total_pages:
            response = self.get(url, params=params)
            page = int(response.get("page", page + 1))
            total_pages = int(response.get("total_pages", page))
            for item in response.get("data", []):
                yield item
            params["page"] = page + 1


class AsyncReqResConnector(AsyncConnector[JSONType]):
    client: AsyncClient

    def __init__(self) -> None:
        self.client = AsyncClient()

    async def _data_request(
        self, method: str, url: str, data: OptionalJSONType = None
    ) -> JSONType:
        response = await getattr(self.client, method)(url, data=data)
        response.raise_for_status()
        return response.json()

    async def post(self, url: str, data: OptionalJSONType = None) -> JSONType:
        return await self._data_request("post", url, data=data)

    async def put(self, url: str, data: OptionalJSONType = None) -> JSONType:
        return await self._data_request("put", url, data=data)

    async def patch(self, url: str, data: OptionalJSONType = None) -> JSONType:
        return await self._data_request("patch", url, data=data)

    async def delete(self, url: str) -> JSONType:
        response = await self.client.delete(url)
        response.raise_for_status()
        return {"code": response.status_code}

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> JSONType:
        params = params or {}
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def list(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> AsyncIterator[JSONType]:
        params = params or {}
        page: int = int(params.get("page", 0))
        total_pages: int = page + 1
        while page < total_pages:
            response = await self.get(url, params=params)
            page = int(response.get("page", page + 1))
            total_pages = int(response.get("total_pages", page))
            for item in response.get("data", []):
                yield item
            params["page"] = page + 1


ReqResEndpoint = Endpoint[JSONType]
AsyncReqResEndpoint = AsyncEndpoint[JSONType]


class UnknownResource(NamedTuple):
    id: int
    name: str
    year: int
    color: str
    pantone_value: str

    def to_body(self) -> Dict[str, Any]:
        resource_data = self._asdict()
        resource_data.pop("id", None)
        return resource_data


class ReqResUnknownResourceCRUD(CRUD[UnknownResource]):
    endpoint: ReqResEndpoint = ReqResEndpoint(BASE_URL, ReqResConnector()).unknown

    def create(self, resource: UnknownResource) -> UnknownResource:
        data = self.endpoint.post(data=resource.to_body())
        return resource._replace(id=int(data["id"]))

    def update(self, resource: UnknownResource, method: str) -> UnknownResource:
        response = getattr(self.endpoint[resource.id], method)(data=resource.to_body())
        response.pop("updatedAt", None)
        response["year"] = int(response["year"])
        return resource._replace(**response)

    def delete(self, resource: UnknownResource) -> UnknownResource:
        response = self.endpoint[resource.id].delete()
        assert response["code"] == 204
        return resource

    def read(self, resource_id: int) -> UnknownResource:
        data = self.endpoint[resource_id].get()
        return UnknownResource(**data["data"])

    def list(self) -> Iterator[UnknownResource]:
        for resource_data in self.endpoint.list():
            yield UnknownResource(**resource_data)


class AsyncReqResUnknownResourceCRUD(AsyncCRUD[UnknownResource]):
    endpoint: AsyncReqResEndpoint = AsyncReqResEndpoint(
        BASE_URL, AsyncReqResConnector()
    ).unknown

    async def create(self, resource: UnknownResource) -> UnknownResource:
        data = await self.endpoint.post(data=resource.to_body())
        return resource._replace(id=int(data["id"]))

    async def update(self, resource: UnknownResource, method: str) -> UnknownResource:
        response = await getattr(self.endpoint[resource.id], method)(
            data=resource.to_body()
        )
        response.pop("updatedAt", None)
        response["year"] = int(response["year"])
        return resource._replace(**response)

    async def delete(self, resource: UnknownResource) -> UnknownResource:
        response = await self.endpoint[resource.id].delete()
        assert response["code"] == 204
        return resource

    async def read(self, resource_id: int) -> UnknownResource:
        data = await self.endpoint[resource_id].get()
        return UnknownResource(**data["data"])

    async def list(self) -> AsyncIterator[UnknownResource]:
        async for resource_data in self.endpoint.list():
            yield UnknownResource(**resource_data)
