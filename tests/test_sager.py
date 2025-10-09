
from dubu_client import DubuClientManager


def test_hent_aktive_sager(dubu_manager: DubuClientManager):
    
    result = dubu_manager.sager.hent_aktive_sager()
    
    assert result is not None, "Failed to retrieve aktive sager"
    assert isinstance(result, dict), "Result should be a dictionary"
    # Check if the response has expected OData structure
    if 'value' in result:
        assert isinstance(result['value'], list), "Result value should be a list of sager"
        assert len(result['value']) == 20, "There should be 20 sager in the list"


def test_soeg_sager(dubu_manager: DubuClientManager):
    
    result = dubu_manager.sager.soeg_sager("2222222222")
    
    assert result is not None, "Failed to retrieve search results"
    assert isinstance(result, dict), "Result should be a dictionary"
    
    # Check if the response has expected OData structure
    assert 'value' in result, "Result should contain 'value' key"
    assert isinstance(result['value'], list), "Result value should be a list of sager"
    assert len(result['value']) == 1, "There should be exactly one sag in the search results"
    
    # Check that the sag contains the expected sagsnavn
    assert result['value'][0]['titel'] == "Test Testesen"

def test_soeg_sager_sammenhaengende_borger_forloeb(dubu_manager: DubuClientManager):

    result = dubu_manager.sager.soeg_sager_sammenhaengende_borger_forloeb()

    assert result is not None, "Failed to retrieve search results"
    assert isinstance(result, dict), "Result should be a dictionary"

    # Check if the response has expected OData structure
    assert 'value' in result, "Result should contain 'value' key"
    assert isinstance(result['value'], list), "Result value should be a list of sager"

def test_hent_sag(dubu_manager: DubuClientManager):

    result = dubu_manager.sager.hent_sag(606094)

    assert result is not None, "Failed to retrieve sag"
    assert isinstance(result, dict), "Result should be a dictionary"
    assert result['id'] == 606094, "Retrieved sag ID does not match"



