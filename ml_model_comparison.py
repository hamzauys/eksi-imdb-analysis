import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. Reading the data
eksi_df = pd.read_csv("data/2008eksi_entry_counts.csv")
imdb_df = pd.read_csv("data/2008imdb_scores.csv")

# 2. Merging
df = pd.merge(eksi_df, imdb_df, on="title")

# 3. Necessary columns and cleaning
df = df[["title", "estimated_entry_count", "imdb_score"]].dropna()
df["estimated_entry_count"] = df["estimated_entry_count"].astype(float)
df["imdb_score"] = df["imdb_score"].astype(float)

# 4.Test Part
X = df[["estimated_entry_count"]]
y = df["imdb_score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Linear Regression Model
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

print(" Linear Regression:")
print("MSE:", mean_squared_error(y_test, y_pred_lr))
print("R²:", r2_score(y_test, y_pred_lr))
    
# 6. Knn Regressor Model
knn = KNeighborsRegressor(n_neighbors=3)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

print("\n KNN Regressor (k=3):")
print("MSE:", mean_squared_error(y_test, y_pred_knn))
print("R²:", r2_score(y_test, y_pred_knn))
