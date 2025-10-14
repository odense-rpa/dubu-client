import json

from datetime import datetime
from datetime import timezone

from dubu_client.client import DubuClient

from .skabeloner import _opret_aktivitet


class AktivitetClient:
    def __init__(self, dubu_client: DubuClient) -> None:
        self.client = dubu_client

    def hent_aktiviter_for_sag(self, sags_id: int) -> list[dict]:
        """Henter aktiviteter for en given sag ID."""
        endpoint = f"/odata/Aktivitet/Default.GetBySag(Id={sags_id})"
        response = self.client.get(endpoint)

        response.raise_for_status()
        data = response.json()

        return data.get("value", [])

        return response.json() if response.status_code == 200 else None

    def opret_aktivitet(
        self,
        sags_id: int,
        type: str,
        undertype: str,
        beskrivelse: str,
        status: str = "Aktiv",
        prioritet: str = "Lav",
        notat: str = "",
        **kwargs,
    ) -> dict:
        response = self.client.get(f"api/sager/aktivitetCreate/{sags_id}")
        response.raise_for_status()
        sagsreference = response.json()

        # Borgers relation til sag
        response = self.client.get(
            f"/api/parter/borger/getBorgerAndRelationToSag/{sagsreference['personId']}?sagId={sagsreference['sagId']}"
        )
        response.raise_for_status()
        borger_relation = response.json()
        borger_relation["laast"] = True

        # Hent bruger
        response = self.client.get("/api/organisation/bruger/currentuser")
        response.raise_for_status()
        bruger = response.json()

        # Status muligheder
        response = self.client.get(
            "/api/klassifikation/aktivitetstatuser?onlyUserOptions=true"
        )
        response.raise_for_status()
        status_muligheder = response.json()

        status_objekt = next(
            (s for s in status_muligheder if s["titel"] == status), None
        )

        # Aktivitetstyper
        response = self.client.get(
            "/api/klassifikation/aktivitetTypeKlasseRelationResult"
        )
        response.raise_for_status()
        aktivitetstyper = response.json()

        type_objekt = next(
            (t for t in aktivitetstyper.get("typer", []) if t["titel"] == type), None
        )
        if not type_objekt:
            raise ValueError(f"Aktivitetstype '{type}' ikke fundet")

        undertyper = aktivitetstyper.get("undertyper", {}).get(
            type_objekt["brugervendtNoegle"], None
        )
        if not undertyper:
            raise ValueError(f"Ingen undertyper fundet for aktivitetstype '{type}'")

        undertype_objekt = next(
            (ut for ut in undertyper if ut["titel"] == undertype), None
        )
        if not undertype_objekt:
            raise ValueError(
                f"Aktivitetens undertype '{undertype}' ikke fundet under type '{type}'"
            )

        # Prioriteter
        response = self.client.get("/api/klassifikation/aktivitetPrioriteter")
        response.raise_for_status()
        prioriteter = response.json()

        prioritet_objekt = next(
            (p for p in prioriteter if p["titel"] == prioritet), None
        )
        if not prioritet_objekt:
            raise ValueError(f"Aktivitetens prioritet '{prioritet}' ikke fundet")

        opret_obj = json.loads(_opret_aktivitet)

        opret_obj["status"] = status_objekt
        opret_obj["sagReference"] = sagsreference
        opret_obj["prioritet"] = prioritet_objekt
        opret_obj["primaerBehandlerNavn"] = bruger["orgBruger"]["navn"]
        opret_obj["primaerBehandlerId"] = bruger.get("id")
        opret_obj["vedroerer"] = [borger_relation]
        opret_obj["type"] = type_objekt
        opret_obj["undertype"] = undertype_objekt
        opret_obj["notat"] = notat
        opret_obj["beskrivelse"] = beskrivelse
        opret_obj["haendelsesDato"] = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )

        # Add kwargs to opret_obj
        for key, value in kwargs.items():
            opret_obj[key] = value

        # Opret objektet i DUBU
        response = self.client.post("/api/aktiviteter", json=opret_obj)
        response.raise_for_status()

        # Response is an int in a string
        aktivitet_id = int(response.text.strip('"'))

        aktivitet_response = self.client.get(f"/api/aktiviteter/{aktivitet_id}")
        aktivitet_response.raise_for_status()

        return aktivitet_response.json()
