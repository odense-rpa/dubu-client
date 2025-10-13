import pytest
import os

from dubu_client import DubuClientManager


@pytest.fixture(scope="session")
def dubu_manager() -> DubuClientManager:
    """Fixture that provides a logged-in DubuClient for tests."""
    login = os.getenv("DUBU_USER")
    password = os.getenv("DUBU_PASSWORD")
    idp = os.getenv("DUBU_IDP")

    assert login

    manager = DubuClientManager(login, password, idp)
    assert manager._client._client.cookies, "Login failed - no cookies set after login"
    return manager
