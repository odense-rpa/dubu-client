from typing import Optional
from urllib.parse import urlencode
from dubu_client.client import DubuClient

class OrgBrugerClient:
    def __init__(self, dubu_client: DubuClient) -> None:
        self.client = dubu_client

    def hent_org_bruger(self, org_bruger_id: int) -> Optional[dict]:
        """
        Hent information om primaer behandler baseret på ID.
        
        Args:
            behandler_id: ID på den behandler der skal hentes
            
        Returns:
            Dict med behandler data eller None hvis ikke fundet
        """
        endpoint = f"api/administration/bruger/orgBruger//{org_bruger_id}"
        response = self.client.get(endpoint)
        return response.json() if response.status_code == 200 else None