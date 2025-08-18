from dubu_client.functionality.sag import SagClient
from .client import DubuClient

class DubuClientManager:

    def __init__(
            self, 
            username: str
    ) -> None:                
        # Initialize client - this will block until login completes (10-35 seconds)
        self._client = DubuClient(username)
        self._sag_client = SagClient(dubu_client=self._client)
    