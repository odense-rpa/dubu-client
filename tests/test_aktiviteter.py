import pytest
import os

from dubu_client import DubuClientManager


def test_hent_aktiviteter_for_sag(dubu_manager: DubuClientManager):

    result = dubu_manager.aktiviteter.hent_aktiviter_for_sag(606094)

    assert result is not None, "Kunne ikke hente aktiviteter for sag"



def test_opret_aktivitet_henvendelse(dubu_manager: DubuClientManager):
    pass
