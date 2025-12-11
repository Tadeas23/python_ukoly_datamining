import csv

with open("literatura.csv", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    next(reader)  # přeskočí hlavičku (pokud tam je)

    # spočítáme řádky, kde není prázdný první sloupec
    pocet = sum(1 for row in reader if row[0].strip() != "")

print("Počet knih:", pocet)
