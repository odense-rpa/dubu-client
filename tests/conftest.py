import pytest
import os

from dubu_client import DubuClientManager


@pytest.fixture
def dubu_manager() -> DubuClientManager:
    """Fixture that provides a logged-in DubuClient for tests."""
    login = os.getenv("DUBU_USER")
    idp = os.getenv("DUBU_IDP")

    assert login

    manager = DubuClientManager(login, idp)
    assert manager._client._client.cookies, "Login failed - no cookies set after login"
    return manager
