from dubu_client import DubuClientManager

def test_hent_org_bruger(dubu_manager: DubuClientManager):

    result = dubu_manager.brugere.hent_org_bruger(30344)

    assert result is not None, "Failed to retrieve primaer behandler"
    assert isinstance(result, dict), "Result should be a dictionary"
    assert result['id'] == 30344, "Retrieved behandler ID does not match"

def test_soeg_org_bruger(dubu_manager: DubuClientManager):    
    result = dubu_manager.brugere.soeg_org_bruger("cdld", top=1)
    
    assert result["@odata.count"] > 0, "No users found with the given initialer"
    for bruger in result["value"]:
        assert 'email' in bruger, "Bruger should have an email field"
        assert 'fuldeNavn' in bruger, "Bruger should have a fuldeNavn field"

def test_soeg_modtager_bruger(dubu_manager: DubuClientManager):
    result = dubu_manager.brugere.soeg_modtager_bruger("Christian de Laurent Drachmann")
    
    assert isinstance(result, list), "Result should be a list"
    assert len(result) > 0, "No users found with the given name"    