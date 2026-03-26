import pytest

from dubu_client import DubuClientManager

def test_opret_advisering(dubu_manager: DubuClientManager):
    modtager = dubu_manager.brugere.soeg_modtager_bruger("Christian de Laurent Drachmann")[0]
    sag = dubu_manager._client.get("api/sager/606094").json()       

    try:
        dubu_manager.advisering.opret_advisering(
            sags_reference=sag["sagReference"],
            titel="Test Advisering- RPA",
            type="PersonligAdvisering",
            ansvar="Sagsbehandler",
            beskrivelse="Dette er en test advisering oprettet via RPA",
            modtager=modtager
        )
    except Exception as e:
        pytest.fail(f"Failed to create advisering: {e}")
    