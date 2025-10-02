import pandas as pd

# Načtení dat
file_path = "ockovani-demografie.csv"  # soubor dej do stejné složky, kde máš skript
df = pd.read_csv(file_path)

# Filtrování na základní očkování (2 dávky)
df_2davky = df[df["poradi_davky"] == 2]

# Agregace podle pohlaví (součet počtů dávek)
agg = df_2davky.groupby("pohlavi")["pocet_davek"].sum()

# Přepočet na procenta
percenta = agg / agg.sum() * 100

# Výpis do konzole
print("Základní očkování (2 dávky):")
for pohlavi, pocet in agg.items():
    if pohlavi == "M":
        print(f"Muži: {pocet:,} osob ({percenta[pohlavi]:.2f} %)")
    elif pohlavi == "Z":
        print(f"Ženy: {pocet:,} osob ({percenta[pohlavi]:.2f} %)")
    else:
        print(f"Ostatní ({pohlavi}): {pocet:,} osob ({percenta[pohlavi]:.2f} %)")
