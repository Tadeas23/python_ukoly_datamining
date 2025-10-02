import pandas as pd
import matplotlib.pyplot as plt

# Načtení dat
file_path = "ockovani-demografie.csv"
df = pd.read_csv(file_path)

# Filtrování na základní očkování (2 dávky)
df_2davky = df[df["poradi_davky"] == 2].copy()

# Agregace
agg = df_2davky.groupby("pohlavi")["pocet_davek"].sum()
agg_vek = df_2davky.groupby(["pohlavi", "vekova_skupina"])["pocet_davek"].sum()

df_2davky["datum"] = pd.to_datetime(df_2davky["datum"])
df_2davky["rok"] = df_2davky["datum"].dt.year
agg_rok = df_2davky.groupby(["pohlavi", "rok"])["pocet_davek"].sum()

# Přepočet na procenta (není potřeba pro grafy, ale nechávám pro výpisy)
percenta = agg / agg.sum() * 100
percenta_vek = agg_vek / agg_vek.sum() * 100
percenta_rok = agg_rok / agg_rok.sum() * 100

# ----------------- VIZUALIZACE V JEDNÉ STRÁNCE -----------------
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Očkování (2 dávky) – přehled", fontsize=16)

# 1) Koláčový graf podle pohlaví
axes[0,0].pie(
    agg, 
    labels=["Muži" if x=="M" else "Ženy" if x=="Z" else x for x in agg.index], 
    autopct="%.1f%%", startangle=90
)
axes[0,0].set_title("Podíl očkovaných podle pohlaví")

# 2) Sloupcový graf podle věkových kategorií a pohlaví
agg_vek.unstack(0).plot(
    kind="bar", ax=axes[0,1], width=0.8
)
axes[0,1].set_title("Podle věkových skupin a pohlaví")
axes[0,1].set_xlabel("Věková skupina")
axes[0,1].set_ylabel("Počet osob")

# 3) Časový vývoj podle roků a pohlaví
agg_rok.unstack(0).plot(
    kind="line", marker="o", ax=axes[1,0]
)
axes[1,0].set_title("Vývoj podle roku a pohlaví")
axes[1,0].set_xlabel("Rok")
axes[1,0].set_ylabel("Počet osob")
axes[1,0].grid(True)

# 4) Volný graf – třeba celkové počty
axes[1,1].bar(agg.index, agg.values)
axes[1,1].set_title("Celkové počty očkovaných")
axes[1,1].set_xlabel("Pohlaví")
axes[1,1].set_ylabel("Počet osob")

plt.tight_layout(rect=[0, 0, 1, 0.96])  # aby se vešel nadpis
plt.show()
