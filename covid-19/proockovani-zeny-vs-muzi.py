import pandas as pd

# Načtení dat
file_path = "ockovani-demografie.csv"  # soubor dej do stejné složky, kde máš skript
df = pd.read_csv(file_path)

# Filtrování na základní očkování (2 dávky)
df_2davky = df[df["poradi_davky"] == 2]

# Agregace podle pohlaví
agg = df_2davky.groupby("pohlavi")["pocet_davek"].sum()

# Přepočet na procenta
percenta = agg / agg.sum() * 100

# Výpis do konzole
print("Procenta ze základního očkování (2 dávky):")
for pohlavi, hodnota in percenta.items():
    if pohlavi == "M":
        print(f"Muži: {hodnota:.2f} %")
    elif pohlavi == "Z":
        print(f"Ženy: {hodnota:.2f} %")
    else:
        print(f"Ostatní ({pohlavi}): {hodnota:.2f} %")
