import asyncio
from typing import AsyncIterator, Iterator
import pytest
from ezrest.requests import (
    AsyncConnector,
    AsyncEndpoint,
    Connector,
    Endpoint,
    BaseEndpoint,
)

BASE_URL = "http://x.com"


class TestConnector:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method", ["post", "get", "put", "patch", "delete", "list"]
    )
    async def test_connector_not_implemented(self, method: str):
        kwargs = {
            "headers": {"Content-Type": "application/json"},
            "params": {"q": "some_param"},
        }
        async_connector: AsyncConnector = AsyncConnector()
        connector: Connector = Connector()
        with pytest.raises(NotImplementedError):
            call = getattr(async_connector, method)(BASE_URL, **kwargs)
            if method == "list":
                async for _ in call:
                    pass
            else:
                await call
        with pytest.raises(NotImplementedError):
            getattr(connector, method)(BASE_URL, **kwargs)


class TestEndpoint:
    @pytest.mark.parametrize(
        "url,expected_url",
        [
            (f"{BASE_URL}/", BASE_URL),
            (BASE_URL, BASE_URL),
            (f"{BASE_URL}////", BASE_URL),
            (f"{BASE_URL}/api/posts/3///", f"{BASE_URL}/api/posts/3"),
            (
                f"{BASE_URL}/api/posts/3;param?query=y#fragment",
                f"{BASE_URL}/api/posts/3",
            ),
        ],
    )
    def test_sanitize_url(self, url: str, expected_url: str):
        assert BaseEndpoint._sanitize_url(url) == expected_url

    @pytest.mark.parametrize("resource", [None, True, 5, 3.14, "something"])
    def test_get_sub_resource_url(self, resource):
        endpoint = BaseEndpoint(BASE_URL, Connector())
        expected_url = f"{BaseEndpoint._sanitize_url(BASE_URL)}/{str(resource)}"
        assert endpoint._get_sub_resource_url(resource) == expected_url

    @pytest.mark.parametrize("resource", [None, True, 5, 3.14, "something"])
    def test_generate_endpoint(self, resource):
        endpoint = BaseEndpoint(BASE_URL, Connector())
        new_endpoint = endpoint._generate_endpoint(resource)
        self.validate_endpoint(
            endpoint, new_endpoint, endpoint._get_sub_resource_url(resource)
        )

    def test_generate_endpoint_via_dunder(self):
        expected_url = f"{BASE_URL}/posts/420"
        endpoint = BaseEndpoint(BASE_URL, Connector())
        new_endpoint = endpoint._generate_endpoint("posts")._generate_endpoint(420)
        self.validate_endpoint(endpoint, new_endpoint, expected_url)
        new_endpoint = endpoint.posts[420]
        self.validate_endpoint(endpoint, new_endpoint, expected_url)
        new_endpoint = endpoint["posts"][420]
        self.validate_endpoint(endpoint, new_endpoint, expected_url)

    @staticmethod
    def validate_endpoint(endpoint, new_endpoint, expected_url):
        assert type(new_endpoint) == type(endpoint)
        assert new_endpoint.connector == endpoint.connector
        assert new_endpoint.url == expected_url

    def test_compile_url(self):
        endpoint = BaseEndpoint(BASE_URL, Connector())
        endpoint = endpoint.posts["{}"].comments["{}"].replies["{}"]
        expected_url = f"{BASE_URL}/posts/420/comments/69/replies/positive"
        too_few_arguments = [[], [420], [420, 69]]
        for arguments in too_few_arguments:
            with pytest.raises(IndexError):
                endpoint._compile_url(*arguments)
        assert expected_url == endpoint._compile_url(420, 69, "positive")
        assert expected_url == endpoint._compile_url(
            420, 69, "positive", "additional", None, "args"
        )


class TestRequestsModule:
    class MockedConnector(Connector[str]):
        def post(self, url: str) -> str:
            return f"[post] {url}"

        def get(self, url: str) -> str:
            return f"[get] {url}"

        def put(self, url: str) -> str:
            return f"[put] {url}"

        def patch(self, url: str) -> str:
            return f"[patch] {url}"

        def delete(self, url: str) -> str:
            return f"[delete] {url}"

        def list(self, url: str) -> Iterator[str]:
            for i in range(3):
                yield f"[list] {url} {i}"

    @pytest.fixture
    def api(self) -> Endpoint[str]:
        return Endpoint[str](BASE_URL, TestRequestsModule.MockedConnector())

    @pytest.mark.parametrize("method", ["post", "get", "put", "patch", "delete"])
    def test_module(self, api: Endpoint[str], method: str):
        assert getattr(api, method)() == f"[{method}] {api.url}"

    def test_module_list(self, api: Endpoint[str]):
        for i, item in enumerate(api.list()):
            assert item == f"[list] {api.url} {i}"


class TestAsyncRequestsModule:
    class MockedAsyncConnector(AsyncConnector[str]):
        async def post(self, url: str) -> str:
            await asyncio.sleep(0.001)
            return f"[post] {url}"

        async def get(self, url: str) -> str:
            await asyncio.sleep(0.001)
            return f"[get] {url}"

        async def put(self, url: str) -> str:
            await asyncio.sleep(0.001)
            return f"[put] {url}"

        async def patch(self, url: str) -> str:
            await asyncio.sleep(0.001)
            return f"[patch] {url}"

        async def delete(self, url: str) -> str:
            await asyncio.sleep(0.001)
            return f"[delete] {url}"

        async def list(self, url: str) -> AsyncIterator[str]:
            for i in range(3):
                await asyncio.sleep(0.001)
                yield f"[list] {url} {i}"

    @pytest.fixture
    def api(self) -> AsyncEndpoint[str]:
        return AsyncEndpoint[str](
            BASE_URL, TestAsyncRequestsModule.MockedAsyncConnector()
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ["post", "get", "put", "patch", "delete"])
    async def test_module(self, api: AsyncEndpoint[str], method: str):
        assert await getattr(api, method)() == f"[{method}] {api.url}"

    @pytest.mark.asyncio
    async def test_module_list(self, api: AsyncEndpoint[str]):
        i = 0
        async for item in api.list():
            assert item == f"[list] {api.url} {i}"
            i += 1
