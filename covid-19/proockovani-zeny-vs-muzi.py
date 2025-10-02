import pandas as pd
import matplotlib.pyplot as plt

# Načtení CSV souboru
df = pd.read_csv("ockovani-demografie.csv", delimiter=",")

# Filtrování jen na 2. dávku
df_filtered = df[df["poradi_davky"] == 2]

# Sečtení podle pohlaví (absolutní počty)
counts = df_filtered["pohlavi"].value_counts()

# Procenta (na 2 desetinná místa)
percentages = df_filtered["pohlavi"].value_counts(normalize=True) * 100

# Vypsání do konzole
for gender in counts.index:
    print(f"{gender}: {counts[gender]} ({percentages[gender]:.2f} %)")

# Vykreslení koláčového grafu
if not counts.empty:
    plt.figure(figsize=(8, 8))
    plt.pie(
        counts,
        labels=counts.index,
        autopct=lambda pct: f"{pct:.2f}%",
        startangle=90
    )
    plt.title("Zastoupení mužů a žen u 2. dávky očkování")
    plt.show()
else:
    print("Žádná data pro vybranou dávku")
