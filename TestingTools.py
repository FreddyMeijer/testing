"""
Module met hulpmiddelen voor het genereren van testbestanden en logging.

Deze module bevat de klasse `TestingTools`, die automatisch een output- en
loggingmap aanmaakt in de scriptdirectory. Daarnaast ondersteunt de klasse het
downloaden van testpersonen via de API van randomuser.me en het loggen van
activiteiten.
"""

import logging
import pathlib as pl

import requests as rq


class TestingTools:
    """
    Hulpmiddelen voor het genereren van testbestanden en het configureren van logging.

    Deze klasse maakt automatisch de benodigde output- en loggingmappen aan in de
    directory waar het script wordt uitgevoerd. Daarnaast configureert het logging
    zodat berichten naar zowel de console als een logbestand worden geschreven.

    Attributen
    ----------
    script_dir : pathlib.Path
        De directory waarin dit script zich bevindt.
    output_dir : pathlib.Path
        Directory waarin outputbestanden worden opgeslagen.
    logging_dir : pathlib.Path
        Directory waarin logbestanden worden opgeslagen.
    log_file : pathlib.Path
        Pad naar het logbestand (``app.log``).
    """

    def __init__(self):
        """
        Initialiseert de TestingTools klasse.

        De constructor zorgt voor:
        * het instellen van de paden naar script-, output- en loggingdirectory,
        * het aanmaken van de mappen als deze nog niet bestaan,
        * het configureren van logging met zowel console- als bestandshandler.
        """
        self.script_dir = pl.Path(__file__).resolve().parent
        self.output_dir = self.script_dir / "output"
        self.logging_dir = self.script_dir / "logging"

        self.output_dir.mkdir(exist_ok=True)
        self.logging_dir.mkdir(exist_ok=True)

        self.log_file = self.logging_dir / "app.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(self.log_file, encoding="utf-8"),
                logging.StreamHandler()
            ]
        )

    def testbestand_personen(self, aantal: int):
        """
        Download een testbestand met willekeurige personen en sla dit op als CSV.

        Er wordt gebruikgemaakt van de API ``https://randomuser.me`` om testdata
        op te halen. Het resultaat wordt opgeslagen in de outputdirectory als
        ``testpersonen.csv``.

        Parameters
        ----------
        aantal : int
            Het aantal testpersonen dat moet worden opgehaald.

        Raises
        ------
        requests.exceptions.RequestException
            Indien er een fout optreedt tijdens het ophalen van de gegevens.
        """
        testpersonen = self.output_dir / "testpersonen.csv"
        url = f"https://randomuser.me/api/?results={aantal}&format=csv&nat=NL"
        logging.info("Downloading testpersonen van %s", url)
        try:
            response = rq.get(url, timeout=10)
            if response.status_code == 200:
                with open(testpersonen, "wb") as file:
                    file.write(response.content)
                    logging.info("Testpersonen opgeslagen in %s", testpersonen)
        except rq.exceptions.RequestException as e:
            logging.error("Fout bij het downloaden van testpersonen: %s", e)

    def bsn_testbestand(self):
        """
        Genereer een testbestand met geldige en ongeldige BSN-nummers.

        Het bestand wordt opgeslagen als ``bsn_testbestand.csv`` in de outputdirectory.
        Het bestand bevat zowel geldige als ongeldige BSN-nummers voor testdoeleinden.
        """
        bsn_bestand = self.output_dir / "bsn_testbestand.csv"
        bsn_nummers = [
            "123456782",  # Geldig
            "987654321",  # Ongeldig
            "111222333",  # Ongeldig
            "123456789",  # Ongeldig
            "876543210",  # Ongeldig
            "234567890",  # Ongeldig
            "345678901",  # Ongeldig
            "456789012",  # Ongeldig
            "567890123",  # Ongeldig
            "678901234",  # Ongeldig
            "789012345",  # Ongeldig
            "890123456",  # Ongeldig
            "901234567",  # Ongeldig
            "012345678",  # Ongeldig
            "135792468",  # Geldig
            "246813579"   # Geldig
        ]
        with open(bsn_bestand, "w", encoding="utf-8") as file:
            for bsn in bsn_nummers:
                file.write(f"{bsn}\n")
        logging.info("BSN testbestand opgeslagen in %s", bsn_bestand)