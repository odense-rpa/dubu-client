from dubu_client.client import DubuClient
import datetime
import os

class DokumentClient:
    def __init__(self, dubu_client: DubuClient) -> None:
        self.client = dubu_client

    def upload_dokument_til_aktivitet(self, sags_id, dokument_titel: str, filnavn: str, dokument: bytes, aktivitet: dict) -> dict:
        endpoint = "api/filer/upload"
        response = self.client.post(endpoint, files={"file": (filnavn, dokument, "application/octet-stream")})

        if response.status_code != 200:
            raise ValueError(f"File upload failed with status code {response.status_code}")            

        id_list = response.json()
        if id_list:
            dokument_id = id_list[0]
        else:
            raise ValueError("Upload response did not contain an ID")
        
        # Proceed with journaling the document
        payload = {
            "aktivitetsId": aktivitet.get("id"),
            "sagsId": sags_id,
            "dokument": {
                "dokumentegenskaber": {
                    "titel": dokument_titel,
                    "journaliseringsdato": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",  # Current UTC date in ISO format with ms and Z
                },
                "dokumentvariantProd": {
                    "fil": {
                        "id": dokument_id                        
                    },
                    "filFormat": {
                        "brugervendtNoegle": os.path.splitext(filnavn)[1][1:]  # Extract file extension cleanly
                    }
                }
            }
        }    

        endpoint = "api/dokumenter/journalizerDokument"
        response = self.client.post(endpoint, json=payload)
        
        if response.status_code != 200:
            raise ValueError(f"Document journaling failed with status code {response.status_code}")

        return response.json()
