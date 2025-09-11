import pytest
import os

from dubu_client.client import DubuClient
from dubu_client.functionality.aktivitet import AktivitetClient

@pytest.fixture
def logged_in_client():
    """Fixture that provides a logged-in DubuClient for tests."""
    login = os.getenv("DUBU_CLIENT")
    client = DubuClient(login)
    assert client._client.cookies, "Login failed - no cookies set after login"
    return client

def test_hent_aktiviteter_for_sag(logged_in_client):
    client = logged_in_client
    aktivitet_client = AktivitetClient(client)

    result = aktivitet_client.hent_aktiviter_for_sag(606094)

    assert result is not None, "Kunne ikke hente aktiviteter for sag"
