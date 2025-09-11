import pytest
import os

from dubu_client.client import DubuClient
from dubu_client.functionality.aktivitet import AktivitetClient
from dubu_client.functionality.dokument import DokumentClient

@pytest.fixture
def logged_in_client():
    """Fixture that provides a logged-in DubuClient for tests."""
    login = os.getenv("DUBU_CLIENT")
    client = DubuClient(login)
    assert client._client.cookies, "Login failed - no cookies set after login"
    return client

def test_upload_dokument(logged_in_client):
    client = logged_in_client
    aktivitet_client = AktivitetClient(client)
    dokument_client = DokumentClient(client)

    odata = aktivitet_client.hent_aktiviter_for_sag(606094)
    assert odata is not None, "Kunne ikke hente aktiviteter for sag"

    aktiviteter = odata.get('value', []) if odata else []

    aktiviteter_filtered = [a for a in aktiviteter if a.get('beskrivelse') == "Asd"]
    assert aktiviteter_filtered, "Ingen aktiviteter med beskrivelse 'Asd' funnet"

    # Read the test_upload.txt file from the project root as bytes
    with open("test_upload.txt", "rb") as f:
        test_upload_bytes = f.read()

    uploaded_dokument = dokument_client.upload_dokument_til_aktivitet(606094, "Test Upload 4", "test_upload.txt", test_upload_bytes, aktiviteter_filtered[0])
    assert uploaded_dokument is not None, "Dokumentet blev ikke uploaded til DUBU"
    assert isinstance(uploaded_dokument, dict), "Upload returnerede ikke et dict"
