import pandas as pd
import numpy as np
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib

# File paths
FILE_PATH = r"D:\Python\project2\wind_data_combined_2016_2025.csv"
MODEL_PATH = r"D:\Python\project2\model\wind_speed_model.pkl"
METRICS_PATH = r"D:\Python\project2\model\metrics.txt"

# Load CSV Data
def load_data(file_path):
    print("Loading data...")
    return pd.read_csv(file_path)

# Preprocess Dataset
def preprocess_data(df):
    print("Preprocessing data...")

    df = df.replace(' ', np.nan)

    # Select relevant columns
    columns = ['LATITUDE', 'LONGITUDE', 'ELEVATION', 'TEMP', 'DEWP', 'SLP', 'STP', 'MXSPD', 'GUST', 'WDSP']
    df = df[columns].dropna()

    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna()

    X = df[['LATITUDE', 'LONGITUDE', 'ELEVATION', 'TEMP', 'DEWP', 'SLP', 'STP', 'MXSPD', 'GUST']]
    y = df['WDSP']

    return X, y

# Train the Model
def train_model(X_train, y_train):
    print("Training model...")
    model = XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    return model

# Evaluate Model and Save Metrics
def evaluate_model(model, X_test, y_test, metrics_path):
    print("Evaluating model...")
    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    # Print metrics
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"R² Score: {r2:.2f}")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")

    # Save metrics
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    with open(metrics_path, "w") as f:
        f.write(f"Mean Squared Error (MSE): {mse:.4f}\n")
        f.write(f"R² Score: {r2:.4f}\n")
        f.write(f"Mean Absolute Error (MAE): {mae:.4f}\n")

    print(f"Metrics saved to: {metrics_path}")
    return mse, r2, mae

# Save Trained Model
def save_model(model, model_path):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved at: {model_path}")

# Main Execution
def main():
    df = load_data(FILE_PATH)
    X, y = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test, METRICS_PATH)
    save_model(model, MODEL_PATH)

if __name__ == "__main__":
    main()
