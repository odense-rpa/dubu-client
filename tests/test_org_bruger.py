import pytest
import os

from dubu_client.client import DubuClient
from dubu_client.functionality.org_bruger import OrgBrugerClient

@pytest.fixture
def logged_in_client():
    """Fixture that provides a logged-in DubuClient for tests."""
    login = os.getenv("DUBU_CLIENT")
    client = DubuClient(login)
    assert client._client.cookies, "Login failed - no cookies set after login"
    return client

def test_hent_org_bruger(logged_in_client):
    client = logged_in_client
    org_bruger_client = OrgBrugerClient(client)

    result = org_bruger_client.hent_org_bruger(30344)

    assert result is not None, "Failed to retrieve primaer behandler"
    assert isinstance(result, dict), "Result should be a dictionary"
    assert result['id'] == 30344, "Retrieved behandler ID does not match"