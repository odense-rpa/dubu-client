from dubu_client import DubuClientManager

def test_hent_org_bruger(dubu_manager: DubuClientManager):

    result = dubu_manager.brugere.hent_org_bruger(30344)

    assert result is not None, "Failed to retrieve primaer behandler"
    assert isinstance(result, dict), "Result should be a dictionary"
    assert result['id'] == 30344, "Retrieved behandler ID does not match"