from typing import Any, AsyncIterator, Dict, Iterator, Optional
from httpx import AsyncClient, Client
from ezrest.requests import AsyncConnector, AsyncEndpoint, Connector, Endpoint

JSONType = Dict[str, Any]

# The service used in the tests is documented here:
# https://reqres.in/


class ReqResConnector(Connector[JSONType]):
    client: Client

    def __init__(self) -> None:
        self.client = Client()

    def _data_request(self, method: str, url: str, data: JSONType = None) -> JSONType:
        response = getattr(self.client, method)(url, data=data)
        response.raise_for_status()
        return response.json()

    def post(self, url: str, data: JSONType = None) -> JSONType:
        return self._data_request("post", url, data=data)

    def put(self, url: str, data: JSONType = None) -> JSONType:
        return self._data_request("put", url, data=data)

    def patch(self, url: str, data: JSONType = None) -> JSONType:
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
        self, method: str, url: str, data: JSONType = None
    ) -> JSONType:
        response = await getattr(self.client, method)(url, data=data)
        response.raise_for_status()
        return response.json()

    async def post(self, url: str, data: JSONType = None) -> JSONType:
        return await self._data_request("post", url, data=data)

    async def put(self, url: str, data: JSONType = None) -> JSONType:
        return await self._data_request("put", url, data=data)

    async def patch(self, url: str, data: JSONType = None) -> JSONType:
        return await self._data_request("patch", url, data=data)

    async def delete(self, url: str) -> JSONType:
        response = await self.client.delete(url)
        response.raise_for_status()
        return {"code": response.status_code}

    async def get(self, url: str, params: Dict[str, Any] = None) -> JSONType:
        params = params or {}
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def list(
        self, url: str, params: Dict[str, Any] = None
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
