import json

from dubu_client.client import DubuClient
from .skabeloner import _opret_advisering

class AdviseringClient:
    def __init__(self, dubu_client: DubuClient) -> None:
        self.client = dubu_client

    def opret_advisering(
        self,
        sags_reference: dict,
        titel: str,
        type: str,
        ansvar: str,        
        beskrivelse: str,
        modtager: dict,        
    ) -> dict:            

        opret_obj = json.loads(_opret_advisering)
        opret_obj["adviseringsType"] = {
            "brugervendtNoegle": type
        }
        opret_obj["sagReference"] = sags_reference
        opret_obj["ansvar"] = {
            "brugervendtNoegle": ansvar
        }
        opret_obj["titel"] = titel
        opret_obj["beskrivelse"] = beskrivelse
        
        opret_obj["modtager"] = modtager

        response = self.client.post(
            endpoint="api/adviseringer",
            json=opret_obj
        )

        response.raise_for_status()
        return response.json()