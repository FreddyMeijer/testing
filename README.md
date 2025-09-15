# TestingTools

## Overzicht

`TestingTools` is een Python-module met hulpmiddelen voor het genereren
van testbestanden en het configureren van logging.

De klasse maakt automatisch de benodigde **output**- en
**logging**-mappen aan in de directory waar het script wordt
uitgevoerd.\
Daarnaast configureert het logging zodat berichten naar zowel de
**console** als een **logbestand** worden geschreven.\
Met de ingebouwde methode kun je eenvoudig testpersonen downloaden via
de API van [randomuser.me](https://randomuser.me).

------------------------------------------------------------------------

## Installatie

Zorg dat Python 3.10+ geïnstalleerd is en installeer de
afhankelijkheden:

``` bash
pip install requests
```

------------------------------------------------------------------------

## Gebruik

### Voorbeeldscript

``` python
from testingtools import TestingTools


# Maak een sessie aan
sessie = TestingTools()


# Download 100 testpersonen en sla deze op in output/testpersonen.csv
sessie.testbestand_personen(100)


# Test een bestaand BSN-nummer
is_geldig = sessie.test_bsnnummer(123456782)
print("BSN geldig:", is_geldig)


# Genereer een nieuw geldig BSN-nummer
geldig_bsn = sessie.genereer_bsn()
print("Gegenereerd geldig BSN:", geldig_bsn)
```

Na uitvoeren vind je: - `output/testpersonen.csv` met testpersonen -
`logging/app.log` met logmeldingen

### Logging

De logging wordt automatisch ingesteld: - INFO en foutmeldingen
verschijnen in de **console** - Alle berichten worden ook weggeschreven
naar `logging/app.log`

------------------------------------------------------------------------

## Klassen en Methoden

### `class TestingTools`

Hulpmiddelen voor het genereren van testbestanden en het configureren
van logging.

**Attributen** - `script_dir` : de directory waarin dit script zich
bevindt\

- `output_dir` : directory waarin outputbestanden worden opgeslagen\
- `logging_dir` : directory waarin logbestanden worden opgeslagen\
- `log_file` : pad naar het logbestand (`app.log`)

#### `__init__()`

Initialiseert de klasse, maakt directories aan en configureert logging.

#### `testbestand_personen(aantal: int)`

Download een CSV-bestand met willekeurige personen via `randomuser.me`.

Parameters: - `aantal` *(int)* -- het aantal testpersonen dat moet
worden opgehaald

Raises: - `requests.exceptions.RequestException` -- indien er een fout
optreedt bij het ophalen

#### `genereer_bsn() -> str`

Genereert een willekeurig geldig BSN-nummer.

**Returns**

- `str` – een geldig BSN-nummer (string) dat voldoet aan de Nederlandse 11-proef

**Opmerkingen**

- De methode genereert net zo lang willekeurige getallen tot er een geldig BSN gevonden is.

#### `test_bsnnummer(bsn: int) -> bool`

Controleert of een gegeven BSN-nummer geldig is volgens de Nederlandse 11-proef.

**Parameters**

- `bsn` *(int)* – het Burgerservicenummer dat gecontroleerd moet worden

**Returns**

- `bool` – `True` als het BSN geldig is, `False` als het ongeldig is

**Logging**

- Geldig BSN wordt gelogd op INFO-niveau
- Ongeldig BSN wordt gelogd op WARNING-niveau

------------------------------------------------------------------------

## Licentie

Dit project is vrij te gebruiken en te verspreiden onder de
MIT-licentie.
