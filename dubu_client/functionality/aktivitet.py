from dubu_client.client import DubuClient

class AktivitetClient:
    def __init__(self, dubu_client: DubuClient) -> None:
        self.client = dubu_client

    def hent_aktiviter_for_sag(self, sags_id: int) -> list[dict]|None:
        endpoint = f"/odata/Aktivitet/Default.GetBySag(Id={sags_id})"
        response = self.client.get(endpoint)
        return response.json() if response.status_code == 200 else None
    
    def opret_aktivitet(self, sags_id: int, type: str, undertype: str, beskrivelse: str,status: str="Aktiv", notat: str=""):
        pass