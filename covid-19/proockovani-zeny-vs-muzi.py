import pandas as pd

# Načtení dat
file_path = "ockovani-demografie.csv"  # soubor dej do stejné složky, kde máš skript
df = pd.read_csv(file_path)

# Filtrování na základní očkování (2 dávky)
df_2davky = df[df["poradi_davky"] == 2].copy()

# Agregace podle pohlaví (součet počtů dávek)
agg = df_2davky.groupby("pohlavi")["pocet_davek"].sum()

agg_vek = df_2davky.groupby(["pohlavi", "vekova_skupina"])["pocet_davek"].sum()

# převod sloupce datum na datetime typ
df_2davky["datum"] = pd.to_datetime(df_2davky["datum"])
# vytvoření sloupce jen s rokem
df_2davky["rok"] = df_2davky["datum"].dt.year  # to vezme jen rok a ignoruje měsíc a den
agg_rok = df_2davky.groupby(["pohlavi", "rok"])["pocet_davek"].sum()


# Přepočet na procenta
percenta = agg / agg.sum() * 100
percenta_vek = agg_vek / agg_vek.sum() * 100
percenta_rok = agg_rok / agg_rok.sum() * 100

# Výpis do konzole
print("Základní očkování (2 dávky):")
for pohlavi, pocet in agg.items():
    if pohlavi == "M":
        print(f"Muži: {pocet:,} osob ({percenta[pohlavi]:.2f} %)")
    elif pohlavi == "Z":
        print(f"Ženy: {pocet:,} osob ({percenta[pohlavi]:.2f} %)")
    else:
        print(f"Ostatní ({pohlavi}): {pocet:,} osob ({percenta[pohlavi]:.2f} %)")

print("Základní očkování (2 dávky), věkové kategorie:")    
for (pohlavi, vek), pocet in agg_vek.items():
    print(f"{pohlavi}, {vek}: {pocet} osob ({percenta_vek[pohlavi, vek]:.2f} %)")
    
print("Základní očkování (2 dávky), rok očkovaní:")    
for (pohlavi, rok), pocet in agg_rok.items():
    print(f"{pohlavi}, {rok}: {pocet} osob ({percenta_rok[pohlavi, rok]:.2f} %)")





