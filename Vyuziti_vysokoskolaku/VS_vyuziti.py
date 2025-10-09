import pandas as pd
import matplotlib.pyplot as plt

# --- Načtení CSV souborů s opravou kódování ---
absolventi = pd.read_csv("Absolventi_vs.csv", encoding="utf-8-sig")
nezam = pd.read_csv("Zdrojova_data.csv", encoding="utf-8-sig")

print("✅ Načteno Absolventi_vs.csv:", absolventi.shape)
print("✅ Načteno Zdrojova_data.csv:", nezam.shape)

# --- Oprava prvního sloupce (prázdný název) ---
nezam.rename(columns={nezam.columns[0]: "Rok"}, inplace=True)

# --- Převod čísel na numerické hodnoty ---
absolventi["Počet absolventů v rámci Královéhradeckého kraje za rok 2022"] = pd.to_numeric(
    absolventi["Počet absolventů v rámci Královéhradeckého kraje za rok 2022"], errors="coerce"
)
nezam["vysokoškolské vzdělání"] = pd.to_numeric(nezam["vysokoškolské vzdělání"], errors="coerce")

# --- Agregace absolventů podle oboru ---
absolventi_obory = (
    absolventi.groupby("Název studijního oboru")["Počet absolventů v rámci Královéhradeckého kraje za rok 2022"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# --- Výpočet celkového počtu absolventů ---
celkem_absolventi = absolventi["Počet absolventů v rámci Královéhradeckého kraje za rok 2022"].sum()

print(f"👨‍🎓 Počet absolventů (celkem 2022): {celkem_absolventi:,.0f}")

# --- Grafy ---
plt.figure(figsize=(10, 5))

# 1️⃣ Top 10 oborů podle počtu absolventů
plt.subplot(1, 2, 1)
absolventi_obory.plot(kind="barh", color="cornflowerblue")
plt.title("Top 10 oborů podle počtu absolventů (2022)")
plt.xlabel("Počet absolventů")
plt.ylabel("Studijní obor")

# 2️⃣ Vývoj nezaměstnanosti vysokoškoláků v čase
plt.subplot(1, 2, 2)
plt.plot(nezam["Rok"], nezam["vysokoškolské vzdělání"], marker="o", color="tomato")
plt.title("Nezaměstnanost vysokoškoláků v čase")
plt.xlabel("Rok")
plt.ylabel("Počet nezaměstnaných")

plt.tight_layout()
plt.show()
