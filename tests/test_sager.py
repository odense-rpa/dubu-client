import pytest
from dubu_client.client import DubuClient
from dubu_client.functionality.sag import SagClient

@pytest.fixture
def logged_in_client():
    """Fixture that provides a logged-in DubuClient for tests."""
    client = DubuClient("RPA Odense Kommune (NIST)")
    assert client._client.cookies, "Login failed - no cookies set after login"
    return client

def test_dubu_client_login(logged_in_client):
    client = logged_in_client
    activities = client.get("odata/Aktivitet/Default.GetBySag(Id=606094)")
    assert activities, "Failed to retrieve activities"


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

