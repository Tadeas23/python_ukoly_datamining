import csv
import urllib.request
import json
import urllib.parse

def zjisti_jazyk(nazev, autor):
    try:
        # zakódujeme parametry, aby nevadily mezery ani diakritika
        nazev_enc = urllib.parse.quote(nazev)
        autor_enc = urllib.parse.quote(autor)

        url = f"https://openlibrary.org/search.json?title={nazev_enc}&author={autor_enc}"
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

        if "docs" in data and len(data["docs"]) > 0:
            doc = data["docs"][0]
            if "language" in doc:
                kod = doc["language"][0]
                # převod ISO kódu na čitelné jazyky
                preklad = {
                    "eng": "angličtina",
                    "cze": "čeština",
                    "fre": "francouzština",
                    "ger": "němčina",
                    "rus": "ruština",
                    "spa": "španělština",
                }
                return preklad.get(kod, kod)
        return "neznámý"
    except Exception as e:
        print("Chyba u knihy:", nazev, autor, e)  # DEBUG
        return "chyba"


# Načtení CSV
with open("literatura.csv", "r", encoding="utf-8-sig") as infile:
    reader = csv.DictReader(infile, delimiter=";")
    knihy = list(reader)

print("Sloupce v CSV:", reader.fieldnames)


# Přidání nového sloupce
for kniha in knihy:
    jazyk = zjisti_jazyk(kniha["název díla"], kniha["autor"])
    kniha["originální jazyk"] = jazyk

# Uložení do nového CSV
with open("literatura_s_jazykem.csv", "w", encoding="utf-8-sig", newline="") as outfile:
    fieldnames = ["název díla", "autor", "oblast", "originální jazyk"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    writer.writerows(knihy)

print("Hotovo! Soubor 'literatura_s_jazykem.csv' byl vytvořen.")
