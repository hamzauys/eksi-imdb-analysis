import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. Reading the data
eksi_df = pd.read_csv("data/2020eksi_entry_counts.csv")
imdb_df = pd.read_csv("data/2020imdb_scores.csv")

# 2. Merging
df = pd.merge(eksi_df, imdb_df, on="title")

# 3. Necessary columns and cleaning
df = df[["title", "estimated_entry_count", "imdb_score"]].dropna()
df["estimated_entry_count"] = df["estimated_entry_count"].astype(float)
df["imdb_score"] = df["imdb_score"].astype(float)

# 4. Train/Test Split
X = df[["estimated_entry_count"]]
y = df["imdb_score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. KNN Regressor for k = 1, 3, 5
print("KNN Regressor Results:\n")
for k in [1, 3, 5]:
    knn = KNeighborsRegressor(n_neighbors=k)
    knn.fit(X_train, y_train)
    y_pred_knn = knn.predict(X_test)

    mse_knn = mean_squared_error(y_test, y_pred_knn)
    r2_knn = r2_score(y_test, y_pred_knn)

    print(f"k = {k} → MSE: {mse_knn:.4f}, R²: {r2_knn:.4f}")

# 6. Random Forest Regressor with different parameters
print("\nRandom Forest Regressor Comparison:\n")

n_estimators_list = [100, 200, 300]
max_depth_list = [5, 10, None]

for n in n_estimators_list:
    for depth in max_depth_list:
        rf = RandomForestRegressor(n_estimators=n, max_depth=depth, random_state=42)
        rf.fit(X_train, y_train)
        y_pred_rf = rf.predict(X_test)

        mse = mean_squared_error(y_test, y_pred_rf)
        r2 = r2_score(y_test, y_pred_rf)

        print(f"n_estimators = {n}, max_depth = {depth} → MSE: {mse:.4f}, R²: {r2:.4f}")
