from typing import Optional
from urllib.parse import urlencode
from dubu_client.client import DubuClient

class OrgBrugerClient:
    def __init__(self, dubu_client: DubuClient) -> None:
        self.client = dubu_client

    def _build_query_endpoint(self, base_endpoint: str, query_params: dict) -> str:
        """
        Build endpoint with properly encoded query parameters.
        
        Args:
            base_endpoint: The base endpoint name
            query_params: Dictionary of query parameters
            
        Returns:
            Complete endpoint with encoded query string
        """
        query_string = urlencode(query_params, safe='(),/$;=')
        # Replace + with %20 for space encoding to match expected format
        query_string = query_string.replace('+', '%20')
        return f"{base_endpoint}?{query_string}"

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
    
    def soeg_org_bruger(self, initialer: str, top=1, skip=0) -> list[dict]:
        query_params = {
            '$format': 'application/json;odata.metadata=none',
            '$top': str(top),
            '$skip': str(skip),
            '$select': 'email,telefon,gyldigTil,fuldeNavn,brugernavn,mobiltelefon,medlemsskaber,id',
            '$orderby': 'fuldeNavn asc',
            '$filter': f"startswith(email,'{initialer}')",
            '$count': 'true'
        }
        
        endpoint = self._build_query_endpoint(
            "odata/OrgBruger/Default.GetByKommune",
            query_params
        )
        
        response = self.client.get(endpoint)
        return response.json()
    
    def soeg_modtager_bruger(self, søge_term, initialer) -> dict|None:
        url_encoded_navn = urlencode({'term': søge_term}, safe='(),/$;=').replace('+', '%20')
        endpoint = f"api/organisation/bruger/suggested?{url_encoded_navn}"
        response = self.client.get(endpoint)
        
        resultater = response.json()

        bruger = next(
            (bruger for bruger in resultater if initialer in bruger.get('orgBruger').get('adresse').get('emailAdresse', '')),
            None
        )

        return bruger