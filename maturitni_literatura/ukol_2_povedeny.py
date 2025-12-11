import pandas as pd
import matplotlib.pyplot as plt

# Načtení CSV souboru
# důležité je nastavit delimiter=";" protože máš oddělovač středník
df = pd.read_csv("literatura.csv", delimiter=";")

# Sečteme počet děl podle oblasti
oblast_counts = df["oblast"].value_counts()

# Vykreslení koláčového grafu
plt.figure(figsize=(8, 8))
plt.pie(
    oblast_counts,
    labels=oblast_counts.index,
    autopct='%1.1f%%',   # procenta s jedním desetinným místem
    startangle=90        # začátek od shora
)
plt.title("Zastoupení literatury podle oblasti")
plt.show()
