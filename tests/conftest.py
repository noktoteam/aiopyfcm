import pytest


@pytest.fixture(autouse=True)
def patch_httpx(respx_mock):
    pass
