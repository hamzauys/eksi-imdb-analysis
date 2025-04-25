# analyze_combined_data.py – Analyze the relationship between Ekşi entry count and IMDb score

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

# 1. Read data
eksi_df = pd.read_csv("data/eksi_entry_counts.csv")  
imdb_df = pd.read_csv("data/imdb_scores.csv")

# 2. Merge on title
merged = pd.merge(eksi_df, imdb_df, on="title")

# 3. Drop missing
merged.dropna(subset=["estimated_entry_count", "imdb_score"], inplace=True)

# 4. Convert types
merged["estimated_entry_count"] = merged["estimated_entry_count"].astype(int)
merged["imdb_score"] = merged["imdb_score"].astype(float)

# 5. Plot scatter + regression line
plt.figure(figsize=(8, 5))
x = merged["estimated_entry_count"]
y = merged["imdb_score"]
plt.scatter(x, y, color="blue", label="Data Points")

# Regression line
m, b = np.polyfit(x, y, 1)
plt.plot(x, m * x + b, color="red", linestyle="--", label=f"Trend Line: y = {m:.2f}x + {b:.2f}")

plt.xticks(np.arange(0, x.max() + 250, 250))  # 0 to max value at 250 intervals

# Labels and styling
plt.xlabel("Pre-release Entry Count")
plt.ylabel("IMDb Score")
plt.title("Entry Count vs IMDb Score")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/entry_vs_imdb.png")
plt.show()

# 6. Pearson Correlation
corr, p_value = pearsonr(x, y)
print(f"\n Pearson Correlation: {corr:.3f}")
print(f" P-value: {p_value:.4f}")
