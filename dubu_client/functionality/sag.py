from typing import Optional, List
from urllib.parse import urlencode
from dubu_client.client import DubuClient

class SagClient:
    def __init__(self, dubu_client: DubuClient) -> None:
        self.client = dubu_client

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
        
        query_string = urlencode(query_params, safe='(),/$;=')
        # Replace + with %20 for space encoding to match expected format
        query_string = query_string.replace('+', '%20')
        endpoint = f"Sag?{query_string}"
        response = self.client.get(endpoint)
        return response.json()

    def hent_sag(self, sag_id: str) -> Optional[dict]:
        # TODO: Implementer
        endpoint = f"sag/{sag_id}"
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
        
        query_string = urlencode(query_params, safe='(),/$;=')
        # Replace + with %20 for space encoding to match expected format
        query_string = query_string.replace('+', '%20')
        endpoint = f"Sag?{query_string}"
        response = self.client.get(endpoint)
        return response.json()