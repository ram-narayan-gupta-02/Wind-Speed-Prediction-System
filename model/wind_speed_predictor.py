
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import xgboost as xgb
import pickle
import os

# ----------------- Load Dataset -----------------
df = pd.read_csv(r"Dataset\clean_wind_data.csv")
print("\n✅ Dataset Loaded:", df.shape)

# ----------------- Features and Target -----------------
features = ['lat', 'lon', 'altitude', 'month', 'year']
target = 'wind_speed'

X = df[features]
y = df[target]

# ----------------- Train-Test Split -----------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----------------- Train XGBoost Model -----------------
model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=8,
    learning_rate=0.1,
    n_jobs=-1,
    random_state=42
)
model.fit(X_train, y_train)

# ----------------- Predictions -----------------
y_pred = model.predict(X_test)

# ----------------- Error Metrics -----------------
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# ----------------- Save Model to .pkl -----------------
os.makedirs("model", exist_ok=True)
with open("model/wind_speed_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n✅ XGBoost Model saved as 'wind_speed_model.pkl'")

# ----------------- Save Error Metrics to .txt -----------------
with open("model/metrics.txt", "w") as f:
    f.write("Wind Speed Prediction Model (XGBoost) - Error Metrics\n")
    f.write(f"Mean Squared Error (MSE): {mse:.2f}\n")
    f.write(f"Mean Absolute Error (MAE): {mae:.2f} m/s\n")
    f.write(f"R² Score: {r2:.2f}\n")

print("✅ Error metrics saved as 'metrics.txt'")
