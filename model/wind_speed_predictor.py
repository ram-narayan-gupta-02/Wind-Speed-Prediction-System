
import pandas as pd
import lightgbm as lgb
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 📂 Step 1: Load the dataset
df = pd.read_csv("cleaned_wind_data.csv")  # Change to your CSV path if needed

# 🎯 Step 2: Define input features and target
features = ['lat', 'lon', 'altitude_m', 'year', 'month', 'day']
target = 'wind_speed'

X = df[features]
y = df[target]

# ✂️ Step 3: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🚀 Step 4: Train LightGBM model
model = lgb.LGBMRegressor(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=8,
    num_leaves=31,
    random_state=42
)
model.fit(X_train, y_train)

# 🔮 Step 5: Predict and evaluate
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 💾 Step 6: Save model to .pkl
joblib.dump(model, "model/wind_speed_model.pkl")

# 📝 Step 7: Save metrics to metrics.txt
with open("model/metrics.txt", "w", encoding="utf-8") as f:
    f.write(f"MSE: {mse:.4f}\n")
    f.write(f"MAE: {mae:.4f} m/s\n")
    f.write(f"R² Score: {r2:.4f}\n") 

print("✅ Model saved as wind_speed_model.pkl")
print("✅ Metrics written to metrics.txt")
