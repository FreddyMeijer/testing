"""
Module met hulpmiddelen voor het genereren van testbestanden en logging.

Deze module bevat de klasse `TestingTools`, die automatisch een output- en
loggingmap aanmaakt in de scriptdirectory. Daarnaast ondersteunt de klasse het
downloaden van testpersonen via de API van randomuser.me en het loggen van
activiteiten.
"""

import logging
import random
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

    def genereer_bsn(self):
        """
        Genereer een willekeurig geldig BSN-nummer.


        Er wordt een willekeurig getal van 10 cijfers samengesteld. Het resultaat
        wordt gecontroleerd met de methode `test_bsnnummer`. Alleen een geldig BSN
        volgens de 11-proef wordt geretourneerd.


        Returns
        -------
        str
        Een geldig BSN-nummer als string.
        """
        bsn = ""
        while True:
            bsn = "".join(str(random.randint(0, 9)) for _ in range(9))
            if self.test_bsnnummer(int(bsn)):
                return bsn

    def test_bsnnummer(self, bsn: int):
        """
        Controleer of een gegeven BSN-nummer geldig is volgens de 11-proef.


        De functie gebruikt de Nederlandse 11-proef om te verifiëren of het
        BSN-nummer correct is. Er wordt gelogd of het nummer geldig of ongeldig
        is.


        Parameters
        ----------
        bsn : int
        Het Burgerservicenummer dat gecontroleerd moet worden.


        Returns
        -------
        bool
        `True` als het BSN geldig is volgens de 11-proef, `False` als het ongeldig is.
        """
        bsnstring = str(bsn).zfill(9)

        totaal = (int(bsnstring[0]) * 9)+(int(bsnstring[1]) * 8)+(int(bsnstring[2]) * 7)+(int(bsnstring[3]) * 6)+(int(
            bsnstring[4]) * 5)+(int(bsnstring[5]) * 4)+(int(bsnstring[6]) * 3)+(int(bsnstring[7]) * 2)+(int(bsnstring[8]) * -1)

        if totaal % 11 == 0:
            logging.info("BSN nummer %i is geldig", bsn)
            return True
        else:
            logging.warning("BSN nummer %i is ongeldig", bsn)
            return False
