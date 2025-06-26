import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load dataset
df = pd.read_csv(r'D:\Python\ADRDE_Project_update\wind_data_combined_2016_2025.csv', dtype={0: str})

# Convert DATE to datetime
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

# Output folder for images
output_folder = r'D:\Python\ADRDE_Project_update\Graphs&Charts\images'
os.makedirs(output_folder, exist_ok=True)

sns.set(style="whitegrid")

### 1. Temperature Trend
if 'TEMP' in df.columns:
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='DATE', y='TEMP')
    plt.title('Temperature Trend Over Time')
    plt.savefig(os.path.join(output_folder, 'temperature_trend.png'))
    plt.close()

### 2. Wind Speed Distribution
if 'WDSP' in df.columns:
    plt.figure(figsize=(6, 4))
    sns.histplot(data=df, x='WDSP', kde=True)
    plt.title('Wind Speed Distribution')
    plt.savefig(os.path.join(output_folder, 'wind_speed_distribution.png'))
    plt.close()

### 3. Station Location Scatter Plot
if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='LONGITUDE', y='LATITUDE')
    plt.title("Station Location Scatter Plot")
    plt.savefig(os.path.join(output_folder, 'station_location.png'))
    plt.close()

### 4. Elevation Distribution
if 'ELEVATION' in df.columns:
    plt.figure(figsize=(6, 4))
    sns.histplot(data=df, x='ELEVATION', kde=True)
    plt.title('Elevation Distribution')
    plt.savefig(os.path.join(output_folder, 'elevation_distribution.png'))
    plt.close()

### 5. Max & Min Temperature Line Plot
if 'MAX' in df.columns and 'MIN' in df.columns:
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='DATE', y='MAX', label='Max Temp')
    sns.lineplot(data=df, x='DATE', y='MIN', label='Min Temp')
    plt.title('Max and Min Temperature Over Time')
    plt.legend()
    plt.savefig(os.path.join(output_folder, 'max_min_temperature.png'))
    plt.close()

### 6. Pairplot for Numerical Columns
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
if len(numeric_cols) >= 2:
    pairplot_df = df[numeric_cols].dropna().sample(min(5000, len(df)))  # Limit rows for speed
    pairplot = sns.pairplot(pairplot_df, diag_kind='kde')
    pairplot.savefig(os.path.join(output_folder, 'pairplot.png'))
    plt.close()

### 7. Correlation Heatmap
if len(numeric_cols) >= 2:
    plt.figure(figsize=(10, 8))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.savefig(os.path.join(output_folder, 'correlation_heatmap.png'))
    plt.close()

print(f"✅ All charts saved separately in: {output_folder}")
