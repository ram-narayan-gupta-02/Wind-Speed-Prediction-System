import streamlit as st
import pandas as pd
import joblib
import time

# 🗺️ Sorted Indian city coordinates
indian_cities = dict(sorted({
    "New Delhi": (28.6139, 77.2090),
    "Agra": (27.1767, 78.0081),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Jaipur": (26.9124, 75.7873),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Surat": (21.1702, 72.8311),
    "Lucknow": (26.8467, 80.9462),
    "Kanpur": (26.4499, 80.3319),
    "Nagpur": (21.1458, 79.0882),
    "Bhopal": (23.2599, 77.4126),
    "Indore": (22.7196, 75.8577),
    "Patna": (25.5941, 85.1376),
    "Varanasi": (25.3176, 82.9739),
    "Amritsar": (31.6340, 74.8723),
    "Chandigarh": (30.7333, 76.7794),
    "Visakhapatnam": (17.6868, 83.2185),
    "Coimbatore": (11.0168, 76.9558),
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Madurai": (9.9252, 78.1198),
    "Mysore": (12.2958, 76.6394),
    "Dehradun": (30.3165, 78.0322),
    "Shimla": (31.1048, 77.1734),
    "Ranchi": (23.3441, 85.3096),
    "Guwahati": (26.1445, 91.7362),
    "Shillong": (25.5788, 91.8933),
    "Itanagar": (27.0844, 93.6053),
    "Gangtok": (27.3314, 88.6138),
    "Imphal": (24.8170, 93.9368),
    "Aizawl": (23.7271, 92.7176),
    "Kohima": (25.6701, 94.1077),
    "Panaji": (15.4909, 73.8278),
    "Puducherry": (11.9416, 79.8083),
}.items()))

# 📦 Load the trained model
model = joblib.load("model/wind_speed_model.pkl")

# 🎨 Streamlit UI
st.set_page_config(page_title="🌬️ Wind Speed Predictor", layout="centered")
st.title("🌬️ Wind Speed Prediction App")
st.markdown("Predict wind speed (**km/h** and **m/s**) using coordinates, altitude, and date.")

# 🔢 Two-column layout
col1, col2 = st.columns(2)

with col1:
    use_city = st.checkbox("Use Indian City 🏙️", value=True)
    if use_city:
        city = st.selectbox("Choose City", list(indian_cities.keys()), index=0)
        lat, lon = indian_cities[city]
        # 👇 Show coordinates when city is selected
        st.markdown(f"**Latitude:** {lat}°  \n**Longitude:** {lon}°")
    else:
        lat = st.number_input("Latitude (°)", -90.0, 90.0, 28.61)
        lon = st.number_input("Longitude (°)", -180.0, 180.0, 77.21)
    alt = st.number_input("Altitude (m)", min_value=110, max_value=26000, value=110, step=100)

with col2:
    year = st.number_input("Year", min_value=2020, max_value=2100, value=2025)
    month = st.number_input("Month", min_value=1, max_value=12, value=7)
    day = st.number_input("Day", min_value=1, max_value=31, value=17)

# 🔮 Predict button
if st.button("🔍 Predict Wind Speed"):
    input_df = pd.DataFrame({
        'lat': [lat],
        'lon': [lon],
        'altitude_m': [alt],
        'year': [year],
        'month': [month],
        'day': [day]
    })

    with st.spinner("🌀 Predicting wind speed..."):
        time.sleep(1.5)
        prediction_mps = model.predict(input_df)[0]
        prediction_kmph = prediction_mps * 3.6

    st.success(f"🌪️ Predicted Wind Speed:\n\n📌 **{prediction_mps:.2f} m/s**  \n🚗 **{prediction_kmph:.2f} km/h**")
