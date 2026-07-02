# dubu-client

Python-klient til DUBU sagsbehandlingssystem ([www.dubu.dk](https://www.dubu.dk)). Håndterer login via headless browser og eksponerer et HTTP-baseret API til sager, aktiviteter, dokumenter, adviseringer og organisationsbrugere.

> Denne klient er ikke officielt støttet eller godkendt af KMD/DUBU. Brug på eget ansvar.

## Installation

```bash
uv add git+https://github.com/odense-rpa/dubu-client
```

Efter installation skal Playwright-browseren hentes:

```bash
uv run playwright install chromium
```

## Forudsætninger

- Python ≥ 3.13
- Adgang til DUBU med brugernavn og adgangskode
- Chromium (se installation ovenfor)

## Konfiguration

| Variabel | Beskrivelse |
|---|---|
| `DUBU_USER` | Brugernavn til DUBU |
| `DUBU_PASSWORD` | Adgangskode til DUBU |
| `DUBU_IDP` | Identity provider / kommunevælger-værdi på DUBU-loginsiden |

## Brug

`DubuClientManager` er det anbefalede indgangspunkt og eksponerer følgende sub-klienter som egenskaber:

| Egenskab | Beskrivelse |
|---|---|
| `.sager` | Hent sag pr. ID, søg, list aktive sager, hent sammenhængende borgerforløb, rediger sag |
| `.aktiviteter` | Hent alle aktiviteter på en sag, opret ny aktivitet med type, undertype, beskrivelse, status og prioritet |
| `.dokumenter` | Upload fil og journaliser den på en aktivitet på en sag |
| `.advisering` | Opret advisering på en sag med type, titel, beskrivelse, ansvar og modtager |
| `.brugere` | Slå organisationsbruger op pr. ID, søg på initialer/e-mail-præfix, find modtagerbruger pr. navn og initialer |

```python
import asyncio
import os
from dubu_client import DubuClientManager

async def main():
    async with DubuClientManager(
        username=os.environ["DUBU_USER"],
        password=os.environ["DUBU_PASSWORD"],
        idp=os.environ["DUBU_IDP"],
    ) as dubu:
        sag = await dubu.sager.get_sag(sag_id=12345)
        aktiviteter = await dubu.aktiviteter.get_aktiviteter(sag_id=sag["id"])

asyncio.run(main())
```

Login sker via en headless Chromium-browser (Playwright) og tager typisk 10–35 sekunder. Efterfølgende API-kald håndteres via `httpx` med de udtrukne OIOSAML-sessionscookies.

Klienten medfølger bundlede SSL-certifikater (GlobalSign intermediate CA) for at håndtere DUBUs ufuldstændige certifikatkæde.

## Afhængigheder

| Pakke | Formål |
|---|---|
| `playwright` | Headless browser-automatisering til DUBU-login |
| `httpx` | HTTP-klient til alle API-kald efter login |
| `authlib` | OAuth- og autentificeringssupport |

## GDPR og sikkerhed

Klienten behandler personoplysninger fra DUBU, herunder CPR-numre, fulde navne, alder og sagsdata for borgere i det sociale sagsbehandlingssystem. Sørg for at adgangskredentialer opbevares sikkert og at data kun tilgås og opbevares i overensstemmelse med gældende databeskyttelseslovgivning.

## Licens

MIT
