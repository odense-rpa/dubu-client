import pytest
import os

from dubu_client import DubuClientManager


def test_hent_aktiviteter_for_sag(dubu_manager: DubuClientManager):

    result = dubu_manager.aktiviteter.hent_aktiviter_for_sag(606094)

    assert result is not None, "Kunne ikke hente aktiviteter for sag"



def test_opret_aktivitet_henvendelse(dubu_manager: DubuClientManager):
    

    result = dubu_manager.aktiviteter.opret_aktivitet(
        sags_id=606094,
        type="Henvendelse",
        undertype="Faglig",
        beskrivelse="Test oprettelse af henvendelse via API",
        status="Aktiv",
        notat="Dette er et testnotat"
    )

    assert result is not None, "Kunne ikke oprette aktivitet"
    assert result.get("id") is not None, "Aktivitet ID mangler i svaret"
    assert result.get("beskrivelse") == "Test oprettelse af henvendelse via API", "Beskrivelse matcher ikke"
    

