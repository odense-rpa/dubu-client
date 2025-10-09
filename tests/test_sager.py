import pytest
import os

from dubu_client.client import DubuClient
from dubu_client.functionality.sag import SagClient

@pytest.fixture
def logged_in_client():
    """Fixture that provides a logged-in DubuClient for tests."""
    login = os.getenv("DUBU_CLIENT")
    client = DubuClient(login)
    assert client._client.cookies, "Login failed - no cookies set after login"
    return client

def test_hent_aktive_sager(logged_in_client):
    client = logged_in_client
    sag_client = SagClient(client)
    
    result = sag_client.hent_aktive_sager()
    
    assert result is not None, "Failed to retrieve aktive sager"
    assert isinstance(result, dict), "Result should be a dictionary"
    # Check if the response has expected OData structure
    if 'value' in result:
        assert isinstance(result['value'], list), "Result value should be a list of sager"
        assert len(result['value']) == 20, "There should be 20 sager in the list"


def test_soeg_sager(logged_in_client):
    client = logged_in_client
    sag_client = SagClient(client)
    
    result = sag_client.soeg_sager("2222222222")
    
    assert result is not None, "Failed to retrieve search results"
    assert isinstance(result, dict), "Result should be a dictionary"
    
    # Check if the response has expected OData structure
    assert 'value' in result, "Result should contain 'value' key"
    assert isinstance(result['value'], list), "Result value should be a list of sager"
    assert len(result['value']) == 1, "There should be exactly one sag in the search results"
    
    # Check that the sag contains the expected sagsnavn
    assert result['value'][0]['titel'] == "Test Testesen"

def test_soeg_sager_sammenhaengende_borger_forloeb(logged_in_client):
    client = logged_in_client
    sag_client = SagClient(client)

    result = sag_client.soeg_sager_sammenhaengende_borger_forloeb()

    assert result is not None, "Failed to retrieve search results"
    assert isinstance(result, dict), "Result should be a dictionary"

    # Check if the response has expected OData structure
    assert 'value' in result, "Result should contain 'value' key"
    assert isinstance(result['value'], list), "Result value should be a list of sager"

def test_hent_sag(logged_in_client):
    client = logged_in_client
    sag_client = SagClient(client)

    result = sag_client.hent_sag(606094)

    assert result is not None, "Failed to retrieve sag"
    assert isinstance(result, dict), "Result should be a dictionary"
    assert result['id'] == 606094, "Retrieved sag ID does not match"



