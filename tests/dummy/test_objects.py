import asyncio
import pytest
from typing import AsyncIterator, Dict, Iterator, Tuple
from ezrest.objects import AsyncCRUD, CRUD

RESOURCE_NAME = "test_resource"
CRUD_ARGS = ("random_id",)
CRUD_KWARGS = {"sort": "asc", "filter": "name"}


class TestObjectsModule:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method,args,kwargs",
        [
            ["create", (2,), {}],
            ["update", (3,), {}],
            ["delete", (5,), {}],
            ["read", tuple(), {}],
            ["list", tuple(), {}],
        ],
    )
    async def test_crud_not_implemented(self, method: str, args: Tuple, kwargs: Dict):
        async_crud: AsyncCRUD[int] = AsyncCRUD[int]()
        crud: CRUD[int] = CRUD[int]()
        with pytest.raises(NotImplementedError):
            call = getattr(async_crud, method)(*args, **kwargs)
            if method == "list":
                async for _ in call:
                    pass
            else:
                await call
        with pytest.raises(NotImplementedError):
            getattr(crud, method)(*args, **kwargs)


class TestCRUD:
    class MockedCRUD(CRUD[str]):
        def create(self, resource: str) -> str:
            return f"[create] {resource}"

        def update(self, resource: str) -> str:
            return f"[update] {resource}"

        def delete(self, resource: str) -> str:
            return f"[delete] {resource}"

        def read(self, *args, **kwargs) -> str:
            return f"[read] {args} {kwargs}"

        def list(self, *args, **kwargs) -> Iterator[str]:
            for i in range(3):
                yield f"[list][{i}] {args} {kwargs}"

    @pytest.fixture
    def crud(self) -> MockedCRUD:
        return TestCRUD.MockedCRUD()

    @pytest.mark.parametrize("method", ["create", "update", "delete"])
    def test_crud_modification(self, crud: MockedCRUD, method: str):
        assert getattr(crud, method)(RESOURCE_NAME) == f"[{method}] {RESOURCE_NAME}"

    def test_crud_read(self, crud: MockedCRUD):
        assert (
            crud.read(*CRUD_ARGS, **CRUD_KWARGS) == f"[read] {CRUD_ARGS} {CRUD_KWARGS}"
        )

    def test_crud_list(self, crud: MockedCRUD):
        for i, item in enumerate(crud.list(*CRUD_ARGS, **CRUD_KWARGS)):
            assert item == f"[list][{i}] {CRUD_ARGS} {CRUD_KWARGS}"


class TestAsyncCRUD:
    class MockedAsyncCRUD(AsyncCRUD[str]):
        async def create(self, resource: str) -> str:
            await asyncio.sleep(0.001)
            return f"[create] {resource}"

        async def update(self, resource: str) -> str:
            await asyncio.sleep(0.001)
            return f"[update] {resource}"

        async def delete(self, resource: str) -> str:
            await asyncio.sleep(0.001)
            return f"[delete] {resource}"

        async def read(self, *args, **kwargs) -> str:
            await asyncio.sleep(0.001)
            return f"[read] {args} {kwargs}"

        async def list(self, *args, **kwargs) -> AsyncIterator[str]:
            for i in range(3):
                await asyncio.sleep(0.001)
                yield f"[list][{i}] {args} {kwargs}"

    @pytest.fixture
    def crud(self) -> MockedAsyncCRUD:
        return TestAsyncCRUD.MockedAsyncCRUD()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ["create", "update", "delete"])
    async def test_crud_modification(self, crud: MockedAsyncCRUD, method: str):
        assert (
            await getattr(crud, method)(RESOURCE_NAME) == f"[{method}] {RESOURCE_NAME}"
        )

    @pytest.mark.asyncio
    async def test_crud_read(self, crud: MockedAsyncCRUD):
        assert (
            await crud.read(*CRUD_ARGS, **CRUD_KWARGS)
            == f"[read] {CRUD_ARGS} {CRUD_KWARGS}"
        )

    @pytest.mark.asyncio
    async def test_crud_list(self, crud: MockedAsyncCRUD):
        i = 0
        async for item in crud.list(*CRUD_ARGS, **CRUD_KWARGS):
            assert item == f"[list][{i}] {CRUD_ARGS} {CRUD_KWARGS}"
            i += 1
