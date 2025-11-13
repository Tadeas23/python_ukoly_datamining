import pandas as pd
import matplotlib.pyplot as plt
import os

# Funkce pro načtení dat z adresáře souhrn_matematiky nebo detaily_testu
def nacti_data(data_dir):
    data = []
    for year in os.listdir(data_dir):  # Procházíme jednotlivé roky
        if year == "2025":
            continue  # Rok 2025 vynecháme

        year_path = os.path.join(data_dir, year)
        souhrn_path = os.path.join(year_path, "souhrn_matematiky")
        detaily_path = os.path.join(year_path, "detaily_testu")
        zaci_file = os.path.join(year_path, f"{year}_zaci.csv")

        if os.path.exists(souhrn_path):  # Pokud existuje složka souhrn_matematiky
            for file in os.listdir(souhrn_path):
                if file.endswith(".csv"):
                    file_path = os.path.join(souhrn_path, file)
                    print(f"Načítám soubor: {file_path}")
                    try:
                        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
                        df['rok'] = year
                        data.append(df)
                    except Exception as e:
                        print(f"Chyba při načítání souboru {file_path}: {e}")
        elif os.path.exists(detaily_path) and os.path.exists(zaci_file):  # Pokud existuje složka detaily_testu a soubor zaci.csv
            zaci_df = pd.read_csv(zaci_file, sep=';', encoding='utf-8')
            for file in os.listdir(detaily_path):
                if file.endswith(".csv"):
                    file_path = os.path.join(detaily_path, file)
                    print(f"Načítám soubor: {file_path}")
                    try:
                        test_df = pd.read_csv(file_path, sep=';', encoding='utf-8')
                        # Propojení dat na základě prijmeni a jmeno
                        merged_df = pd.merge(test_df, zaci_df, on=['prijmeni', 'jmeno'], how='inner')
                        merged_df['rok'] = year
                        data.append(merged_df)
                    except Exception as e:
                        print(f"Chyba při načítání souboru {file_path}: {e}")
    return pd.concat(data, ignore_index=True) if data else pd.DataFrame()

# Cesta k adresáři s daty
data_dir = "data"

# Načtení dat
data = nacti_data(data_dir)

# Předpokládáme, že data obsahují sloupce: 'skola_zkr' (zkratka školy) a 'zkouska_body' (body ze zkoušky)
if 'skola_zkr' in data.columns and 'zkouska_body' in data.columns:
    # Agregace průměrného skóre podle základní školy
    prumerne_skore = data.groupby('skola_zkr')['zkouska_body'].mean().sort_values(ascending=False)

    # Získání rozsahu let v datech
    roky = data['rok'].unique()
    rozsah_let = f"({min(roky)}-{max(roky)})"
    print(f"Data pocházejí z následujících roků: {', '.join(sorted(roky))}")

    # Vykreslení grafu pro top 10 škol
    plt.figure(figsize=(12, 6))
    prumerne_skore.head(10).plot(kind='bar', color='skyblue')
    plt.title(f'Top 10 ZŠ podle průměrného skóre ze zkoušky {rozsah_let}')
    plt.xlabel('Základní škola')
    plt.ylabel('Průměrné skóre')
    plt.xticks(rotation=45, ha='right')
    plt.grid(visible=True, axis='y', which='major', linewidth=1.0, linestyle='-', color='gray', alpha=0.5)  # Pouze horizontální čáry
    plt.grid(visible=True, axis='y', which='minor', linewidth=0.3, linestyle='--', color='lightgray', alpha=0.3)  # Jemnější čáry
    plt.minorticks_on()
    plt.tight_layout()
    plt.show()

    # Vykreslení grafu pro všechny školy
    plt.figure(figsize=(16, 10))
    prumerne_skore.plot(kind='bar', color='lightgreen')
    plt.title(f'Průměrné skóre ze zkoušky podle základních škol {rozsah_let}')
    plt.xlabel('Základní škola')
    plt.ylabel('Průměrné skóre')
    plt.xticks(rotation=90, ha='right', fontsize=8)
    plt.grid(visible=True, axis='y', which='major', linewidth=1.0, linestyle='-', color='gray', alpha=0.5)  # Pouze horizontální čáry
    plt.grid(visible=True, axis='y', which='minor', linewidth=0.3, linestyle='--', color='lightgray', alpha=0.3)  # Jemnější čáry
    plt.minorticks_on()
    plt.tight_layout()
    plt.show()
else:
    print("Data neobsahují požadované sloupce 'skola_zkr' a 'zkouska_body'. Zkontrolujte strukturu CSV souborů.")