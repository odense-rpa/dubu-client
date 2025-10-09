from dubu_client.functionality.aktivitet import AktivitetClient
from dubu_client.functionality.org_bruger import OrgBrugerClient
from dubu_client.functionality.sag import SagClient
from dubu_client.functionality.dokument import DokumentClient

from .client import DubuClient


class DubuClientManager:
    aktiviteter: AktivitetClient
    brugere: OrgBrugerClient
    sager: SagClient
    dokumenter: DokumentClient

    def __init__(self, username: str, idp: str) -> None:
        # Initialize client - this will block until login completes (10-35 seconds)
        self._client = DubuClient(username, idp)
        self.aktiviteter = AktivitetClient(dubu_client=self._client)
        self.brugere = OrgBrugerClient(dubu_client=self._client)
        self.sager = SagClient(dubu_client=self._client)
        self.dokumenter = DokumentClient(dubu_client=self._client)