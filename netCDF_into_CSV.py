# import os
# import xarray as xr
# import numpy as np
# import pandas as pd

# # 🔹 Define input and output
# years = range(2025, 2026)
# all_dataframes = []

# # 🔹 Update these paths to your real file locations
# uwnd_path_template = r"D:\Python\new\Dataset(Days wise)\uwnd.{year}.nc"
# vwnd_path_template = r"D:\Python\new\Dataset(Days wise)\vwnd.{year}.nc"

# # 🔹 India region: lat 5–40, lon 60–100
# INDIA_LAT_MIN, INDIA_LAT_MAX = 5, 40
# INDIA_LON_MIN, INDIA_LON_MAX = 60, 100

# # 🔁 Loop over years
# for year in years:
#     uwnd_file = uwnd_path_template.format(year=year)
#     vwnd_file = vwnd_path_template.format(year=year)

#     if not os.path.exists(uwnd_file) or not os.path.exists(vwnd_file):
#         print(f"⛔ Missing file for year {year}")
#         continue

#     print(f"📦 Processing year {year}...")

#     # Load NetCDF data
#     ds_u = xr.open_dataset(uwnd_file)
#     ds_v = xr.open_dataset(vwnd_file)

#     u = ds_u['uwnd']  # shape: (time, level, lat, lon)
#     v = ds_v['vwnd']

#     # Filter India region
#     u_india = u.sel(lat=slice(INDIA_LAT_MAX, INDIA_LAT_MIN), lon=slice(INDIA_LON_MIN, INDIA_LON_MAX))
#     v_india = v.sel(lat=slice(INDIA_LAT_MAX, INDIA_LAT_MIN), lon=slice(INDIA_LON_MIN, INDIA_LON_MAX))

#     # Compute wind speed
#     wind_speed = np.sqrt(u_india**2 + v_india**2)

#     # Convert to DataFrame
#     df = wind_speed.to_dataframe(name="wind_speed").reset_index()

#     # Add year tag (optional)
#     df['year'] = year

#     all_dataframes.append(df)

# # 🔹 Combine and Save
# if all_dataframes:
#     final_df = pd.concat(all_dataframes, ignore_index=True)
#     final_df.to_csv("wind_speed_india_2020_2025.csv", index=False)
#     print("✅ File saved as wind_speed_india_2020_2025.csv")
# else:
#     print("⚠️ No data processed. Check if files exist.")



import os
import xarray as xr
import numpy as np
import pandas as pd

# ----------------------- STEP 1: Convert .nc to CSV for each year -----------------------

# 🔹 Define input and output
years = range(2020, 2026)
all_dataframes = []

# 🔹 Path templates
folder_path = r"D:\Python\new\Dataset(Days wise)"
uwnd_template = os.path.join(folder_path, "uwnd.{year}.nc")
vwnd_template = os.path.join(folder_path, "vwnd.{year}.nc")

# 🔹 India region bounds
# 🔹 India region: lat 5–40, lon 60–100
INDIA_LAT_MIN, INDIA_LAT_MAX = 5, 40
INDIA_LON_MIN, INDIA_LON_MAX = 60, 100

output_csv_folder = r"D:\Python\new"

for year in years:
    uwnd_file = uwnd_template.format(year=year)
    vwnd_file = vwnd_template.format(year=year)

    if not os.path.exists(uwnd_file) or not os.path.exists(vwnd_file):
        print(f"❌ Missing file for year {year}")
        continue

    print(f"📦 Processing NetCDF for {year}...")

    try:
        # Load NetCDF files
        ds_u = xr.open_dataset(uwnd_file)
        ds_v = xr.open_dataset(vwnd_file)

        u = ds_u['uwnd']
        v = ds_v['vwnd']

        # Filter for India region
        u_india = u.sel(lat=slice(INDIA_LAT_MAX, INDIA_LAT_MIN), lon=slice(INDIA_LON_MIN, INDIA_LON_MAX))
        v_india = v.sel(lat=slice(INDIA_LAT_MAX, INDIA_LAT_MIN), lon=slice(INDIA_LON_MIN, INDIA_LON_MAX))

        # Compute wind speed
        wind_speed = np.sqrt(u_india**2 + v_india**2)

        # Convert to DataFrame
        df = wind_speed.to_dataframe(name="wind_speed").reset_index()
        df['year'] = year

        # Save individual CSV
        single_year_csv = os.path.join(output_csv_folder, f"wind_data_combined{year}.csv")
        df.to_csv(single_year_csv, index=False)
        print(f"✅ Saved: {single_year_csv}")

    except Exception as e:
        print(f"⚠️ Error processing {year}: {e}")

# ----------------------- STEP 2: Combine all yearly CSVs -----------------------

csv_files = [f"wind_data_combined{year}.csv" for year in range(2020, 2026)]
combined_dfs = []

for file in csv_files:
    path = os.path.join(output_csv_folder, file)
    if os.path.exists(path):
        df = pd.read_csv(path)
        combined_dfs.append(df)
        print(f"✅ Loaded: {file}")
    else:
        print(f"⚠️ File not found: {file}")

# Combine into one DataFrame
if combined_dfs:
    combined_df = pd.concat(combined_dfs, ignore_index=True)
    final_path = os.path.join(output_csv_folder, "wind_data_combined_2020_2025.csv")
    combined_df.to_csv(final_path, index=False)
    print(f"🎉 Final combined CSV saved at: {final_path}")
else:
    print("⚠️ No CSV files were available for merging.")

