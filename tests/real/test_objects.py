import pytest
from tests.real.api import (
    AsyncReqResUnknownResourceCRUD,
    ReqResUnknownResourceCRUD,
    UnknownResource,
)


def assert_resource_field_types(resource: UnknownResource):
    assert isinstance(resource.id, int) and resource.id > 0
    assert isinstance(resource.name, str) and resource.name
    assert isinstance(resource.year, int) and resource.year > 0
    assert isinstance(resource.color, str) and resource.color
    assert isinstance(resource.pantone_value, str) and resource.pantone_value


CREATE_RESOURCE = UnknownResource(
    id=-1, name="metro black", year=2033, color="#010101", pantone_value="77-2038"
)
EXPECTED_READ_RESOURCE = UnknownResource(
    id=2, name="fuchsia rose", year=2001, color="#C74375", pantone_value="17-2031"
)
UPDATE_RESOURCE = UnknownResource(
    id=5, name="turbo white", year=1970, color="#FFFFFFFFFFFF", pantone_value="12-3456"
)


class TestReqResObjects:
    @pytest.fixture
    def crud(self) -> ReqResUnknownResourceCRUD:
        return ReqResUnknownResourceCRUD()

    def test_create(self, crud: ReqResUnknownResourceCRUD):
        response = crud.create(CREATE_RESOURCE)
        assert_resource_field_types(response)
        assert response.id != CREATE_RESOURCE.id
        for field in CREATE_RESOURCE._fields:
            if field == "id":
                continue
            assert getattr(response, field) == getattr(CREATE_RESOURCE, field)

    def test_get_resource(self, crud: ReqResUnknownResourceCRUD):
        assert crud.read(EXPECTED_READ_RESOURCE.id) == EXPECTED_READ_RESOURCE

    def test_list_resources(self, crud: ReqResUnknownResourceCRUD):
        retrieved_items = []
        for resource in crud.list():
            assert_resource_field_types(resource)
            retrieved_items.append(resource)
        assert retrieved_items

    @pytest.mark.parametrize("method", ["put", "patch"])
    def test_update_resource(self, crud: ReqResUnknownResourceCRUD, method: str):
        assert crud.update(UPDATE_RESOURCE, method) == UPDATE_RESOURCE

    def test_delete_resource(self, crud: ReqResUnknownResourceCRUD):
        assert crud.delete(UPDATE_RESOURCE) == UPDATE_RESOURCE


class TestAsyncReqResObjects:
    @pytest.fixture
    def crud(self) -> AsyncReqResUnknownResourceCRUD:
        return AsyncReqResUnknownResourceCRUD()

    @pytest.mark.asyncio(scope="class")
    async def test_create(self, crud: AsyncReqResUnknownResourceCRUD):
        response = await crud.create(CREATE_RESOURCE)
        assert_resource_field_types(response)
        assert response.id != CREATE_RESOURCE.id
        for field in CREATE_RESOURCE._fields:
            if field == "id":
                continue
            assert getattr(response, field) == getattr(CREATE_RESOURCE, field)

    @pytest.mark.asyncio(scope="class")
    async def test_get_resource(self, crud: AsyncReqResUnknownResourceCRUD):
        response = await crud.read(EXPECTED_READ_RESOURCE.id)
        assert response == EXPECTED_READ_RESOURCE

    @pytest.mark.asyncio(scope="class")
    async def test_list_resources(self, crud: AsyncReqResUnknownResourceCRUD):
        retrieved_items = []
        async for resource in crud.list():
            assert_resource_field_types(resource)
            retrieved_items.append(resource)
        assert retrieved_items

    @pytest.mark.asyncio(scope="class")
    @pytest.mark.parametrize("method", ["put", "patch"])
    async def test_update_resource(
        self, crud: AsyncReqResUnknownResourceCRUD, method: str
    ):
        response = await crud.update(UPDATE_RESOURCE, method)
        assert response == UPDATE_RESOURCE

    @pytest.mark.asyncio(scope="class")
    async def test_delete_resource(self, crud: AsyncReqResUnknownResourceCRUD):
        response = await crud.delete(UPDATE_RESOURCE)
        assert response == UPDATE_RESOURCE
