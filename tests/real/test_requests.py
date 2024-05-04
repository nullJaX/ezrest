from httpx import HTTPError
import pytest
from tests.real.api import (
    AsyncReqResConnector,
    AsyncReqResEndpoint,
    BASE_URL,
    ReqResConnector,
    ReqResEndpoint,
)

USER_FIELDS = {"id", "email", "first_name", "last_name", "avatar"}


class TestReqResRequests:
    @pytest.fixture
    def api(self) -> ReqResEndpoint:
        return ReqResEndpoint(BASE_URL, ReqResConnector())

    @pytest.mark.parametrize("params", ({}, {"delay": 1}))
    def test_list_users(self, api: ReqResEndpoint, params):
        general_response = api.users.get()
        total_users = int(general_response["total"])
        user_count = 0
        for user in api.users.list(params=params):
            user_count += 1
            assert all(field in user for field in USER_FIELDS)
        assert user_count == total_users

    def test_get_user(self, api: ReqResEndpoint):
        response = api.users[2].get()
        user_data = response["data"]
        assert all(field in user_data for field in USER_FIELDS)
        assert response == api["users"][2].get()
        assert response == api.users["{}"].get(2)

    def test_get_user_not_found(self, api: ReqResEndpoint):
        with pytest.raises(HTTPError, match="404 Not Found"):
            api.users[420].get()

    def test_login_via_post(self, api: ReqResEndpoint):
        post_data = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        response = api.login.post(data=post_data)
        assert "token" in response

    def test_login_via_post_failed(self, api: ReqResEndpoint):
        post_data = {"email": "peter@klaven"}
        with pytest.raises(HTTPError, match="400 Bad Request"):
            api.login.post(data=post_data)

    @pytest.mark.parametrize("method", ("put", "patch"))
    def test_update(self, api: ReqResEndpoint, method: str):
        put_data = {"name": "mike", "job": "technician"}
        response = getattr(api.users[3], method)(data=put_data)
        for key, value in put_data.items():
            assert response[key] == value
        assert "updatedAt" in response

    def test_delete(self, api: ReqResEndpoint):
        response = api.users[69].delete()
        assert response["code"] == 204


class TestAsyncReqResRequests:
    @pytest.fixture
    def api(self) -> AsyncReqResEndpoint:
        return AsyncReqResEndpoint(BASE_URL, AsyncReqResConnector())

    @pytest.mark.asyncio
    @pytest.mark.parametrize("params", ({}, {"delay": 1}))
    async def test_list_users(self, api: AsyncReqResEndpoint, params):
        general_response = await api.users.get()
        total_users = int(general_response["total"])
        user_count = 0
        async for user in api.users.list(params=params):
            user_count += 1
            assert all(field in user for field in USER_FIELDS)
        assert user_count == total_users

    @pytest.mark.asyncio
    async def test_get_user(self, api: AsyncReqResEndpoint):
        response = await api.users[2].get()
        user_data = response["data"]
        assert all(field in user_data for field in USER_FIELDS)
        assert response == await api["users"][2].get()
        assert response == await api.users["{}"].get(2)

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, api: AsyncReqResEndpoint):
        with pytest.raises(HTTPError, match="404 Not Found"):
            await api.users[420].get()

    @pytest.mark.asyncio
    async def test_login_via_post(self, api: AsyncReqResEndpoint):
        post_data = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        response = await api.login.post(data=post_data)
        assert "token" in response

    @pytest.mark.asyncio
    async def test_login_via_post_failed(self, api: AsyncReqResEndpoint):
        post_data = {"email": "peter@klaven"}
        with pytest.raises(HTTPError, match="400 Bad Request"):
            await api.login.post(data=post_data)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ("put", "patch"))
    async def test_update(self, api: AsyncReqResEndpoint, method: str):
        put_data = {"name": "mike", "job": "technician"}
        response = await getattr(api.users[3], method)(data=put_data)
        for key, value in put_data.items():
            assert response[key] == value
        assert "updatedAt" in response

    @pytest.mark.asyncio
    async def test_delete(self, api: AsyncReqResEndpoint):
        response = await api.users[69].delete()
        assert response["code"] == 204
