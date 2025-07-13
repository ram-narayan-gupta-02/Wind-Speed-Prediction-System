import pandas as pd
import numpy as np

# ---------------------- Step 1: Load Dataset ----------------------
df = pd.read_csv("wind_speed_india_2020_2025.csv", parse_dates=['time'])
print(f"✦️ Loaded data: {df.shape[0]} rows, {df.shape[1]} columns")

# ---------------------- Step 2: Drop unnecessary columns ----------------------
df = df.drop(columns=["time"], errors='ignore')

# ---------------------- Step 3: Drop Duplicates ----------------------
df.drop_duplicates(inplace=True)

# ---------------------- Step 4: Drop or Handle Missing Values ----------------------
df.dropna(subset=['lat', 'lon', 'level', 'wind_speed'], inplace=True)

# ---------------------- Step 5: Outlier Removal (IQR method) ----------------------
Q1 = df['wind_speed'].quantile(0.25)
Q3 = df['wind_speed'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

initial_count = df.shape[0]
df = df[(df['wind_speed'] >= lower_bound) & (df['wind_speed'] <= upper_bound)]
final_count = df.shape[0]
print(f"🧹 Outliers removed: {initial_count - final_count}")

# ---------------------- Step 6: Final Column Selection ----------------------
columns = ['lat', 'lon', 'year', 'month', 'day', 'level', 'wind_speed']
df_final = df[columns].copy()
print(f"✅ Final cleaned data shape: {df_final.shape}")

# ---------------------- Step 7: Save Cleaned CSV ----------------------
df_final.to_csv("clean_wind_data.csv", index=False)
print("📁 Saved: clean_wind_data.csv")


# ---------------------- Step 8: Convert Pressure to Altitude ----------------------
# pressure_to_altitude_m = {
#     1000: 110,
#     925: 762,
#     850: 1468,
#     700: 3012,
#     600: 4216,
#     500: 5574,
#     400: 7010,
#     300: 9164,
#     250: 10483,
#     200: 11783,
#     150: 14014,
#     100: 16000,
#      70: 18287,
#      50: 20000,
#      30: 22000,
#      20: 24000,
#      10: 26000
# }

import pandas as pd

# Load your dataset
df = pd.read_csv("clean_wind_data.csv")  # Replace with your actual filename

# Function to convert pressure (hPa) to altitude (meters) ***
def pressure_to_altitude(pressure_hpa):
    return round(44330 * (1 - (pressure_hpa / 1013.25) ** (1 / 5.255)), 2)

# Apply the function to the 'level' column and create a new 'altitude_m' column
df['altitude_m'] = df['level'].apply(pressure_to_altitude)

# Save the updated dataset
df.to_csv("dataset_with_altitude.csv", index=False)
print("📁 Saved: dataset_with_altitude.csv")


# ---------------------- Step 9: Explore Dataset ----------------------
df = pd.read_csv("dataset_with_altitude.csv")
print(df['lat'].min())
print(df['lat'].max())
print(df['lon'].min())
print(df['lon'].max())
print(df['wind_speed'].max())



# ---------------------- Step 10: again Outlier Detection ----------------------
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("dataset_with_altitude.csv")

# Choose the column to check for outliers
col = 'wind_speed'  # replace with your actual column name

# Calculate Q1, Q3, and IQR
Q1 = df[col].quantile(0.25)
Q3 = df[col].quantile(0.75)
IQR = Q3 - Q1

# Define outlier thresholds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Flag outliers
df['is_outlier'] = (df[col] < lower_bound) | (df[col] > upper_bound)

# Plot: Bar chart for outliers
plt.figure(figsize=(14, 6))
colors = df['is_outlier'].map({True: 'red', False: 'skyblue'})

# If you have an index column, use it for x-axis (or use range(len(df)))
plt.bar(df.index, df[col], color=colors)
plt.axhline(Q1, color='orange', linestyle='--', label='Q1')
plt.axhline(Q3, color='green', linestyle='--', label='Q3')
plt.axhline(upper_bound, color='red', linestyle='--', label='Upper Bound')
plt.axhline(lower_bound, color='red', linestyle='--', label='Lower Bound')

plt.title(f'Outlier Detection in {col}')
plt.xlabel('Record Index')
plt.ylabel('Wind Speed')
plt.legend()
plt.tight_layout()
plt.show()