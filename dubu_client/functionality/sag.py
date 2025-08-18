from typing import Optional
from urllib.parse import urlencode
from dubu_client.client import DubuClient

class SagClient:
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
    
    def hent_sag(self, sags_id: int) -> Optional[dict]:
        """
        Hent sag med angivet sags_id.
        
        Args:
            sags_id: ID på den sag der skal hentes
            
        Returns:
            Dict med sag data eller None hvis ikke fundet
        """
        endpoint = f"api/sager/details/{sags_id}"
        response = self.client.get(endpoint)
        return response.json() if response.status_code == 200 else None

    def soeg_sager(self, query: str, top: int = 20, skip: int = 0) -> dict:
        """
        Søg efter sager med angivet søgeterm.
        
        Args:
            query: Søgeterm at bruge
            top: Antal sager at hente (default: 20)
            skip: Antal sager at springe over for paginering (default: 0)
            
        Returns:
            Dict med sager og metadata
        """
        query_params = {
            '$format': 'application/json;odata.metadata=none',
            '$top': str(top),
            '$skip': str(skip),
            '$select': 'tvang,titel,status,sagstype,id,isSensitive,sagsnummer,sekundaerBehandlerNavne',
            '$expand': 'primaerPerson($select=alder,cprnr,fornavn,mellemnavn,efternavn,id,organisationsnavn,fuldeNavn,navn),primaerBehandler,foerstkommendeFrist($select=fristDato,id)',
            '$orderby': 'id desc',
            'search': query,
            '$filter': "((status/brugervendtNoegle ne 'SagStatus2') and (status/brugervendtNoegle ne 'SagStatus5') and (status/brugervendtNoegle ne 'SagStatus6') and (status/brugervendtNoegle ne 'SagStatus7'))",
            '$count': 'true'
        }
        
        endpoint = self._build_query_endpoint("odata/Sag", query_params)
        response = self.client.get(endpoint)
        return response.json()
    
    def hent_aktive_sager(self, top: int = 20, skip: int = 0) -> dict:
        """
        Hent aktive sager med standard filtering og expansion.
        
        Args:
            top: Antal sager at hente (default: 20)
            skip: Antal sager at springe over for paginering (default: 0)
            
        Returns:
            Dict med sager og metadata
        """
        query_params = {
            '$format': 'application/json;odata.metadata=none',
            '$top': str(top),
            '$skip': str(skip),
            '$select': 'tvang,titel,status,sagstype,id,isSensitive,sagsnummer,sekundaerBehandlerNavne',
            '$expand': 'primaerPerson($select=alder,cprnr,fornavn,mellemnavn,efternavn,id,organisationsnavn,fuldeNavn,navn),primaerBehandler,foerstkommendeFrist($select=fristDato,id)',
            '$orderby': 'id desc',
            '$filter': "((status/brugervendtNoegle ne 'SagStatus2') and (status/brugervendtNoegle ne 'SagStatus5') and (status/brugervendtNoegle ne 'SagStatus6') and (status/brugervendtNoegle ne 'SagStatus7'))",
            '$count': 'true'
        }
        
        endpoint = self._build_query_endpoint("odata/Sag", query_params)
        response = self.client.get(endpoint)
        return response.json()

    def soeg_sager_sammenhaengende_borger_forloeb(self) -> dict:
        """
        Hent sager for sammenhængende borgerforløb.
        
        Returns:
            Dict med sager og metadata
        """

        query_params = {
            '$format': 'application/json;odata.metadata=none',
            '$select': 'tvang,titel,status,sagstype,id,isSensitive,sagsnummer,sekundaerBehandlerNavne',
            '$expand': 'primaerPerson($select=alder,cprnr,fornavn,mellemnavn,efternavn,id,organisationsnavn,fuldeNavn,navn),primaerBehandler,foerstkommendeFrist($select=fristDato,id)',
            '$orderby': 'id desc',
            '$filter': "((afdeling/orgEnhedId eq 365449 or afdeling/orgEnhedId eq 366029 or afdeling/orgEnhedId eq 365726 or afdeling/orgEnhedId eq 365464) and (status/brugervendtNoegle eq 'SagStatus1'))",
            '$count': 'true'
        }

        endpoint = self._build_query_endpoint("odata/Sag", query_params)
        response = self.client.get(endpoint)
        return response.json()
    