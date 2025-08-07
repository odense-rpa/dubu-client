from typing import Optional, List
from client import DubuClient

class SagClient:
    def __init__(self, dubu_client: DubuClient) -> None:
        self.client = dubu_client

    def soeg_sager(self, query: str) -> List[dict]:
        # TODO: Implementer
        endpoint = f"sag/soeg?query={query}"
        response = self.client.get(endpoint)
        return response.json().get('results', [])

    def hent_sag(self, sag_id: str) -> Optional[dict]:
        # TODO: Implementer
        endpoint = f"sag/{sag_id}"
        response = self.client.get(endpoint)
        return response.json()