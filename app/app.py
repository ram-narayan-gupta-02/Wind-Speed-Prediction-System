import streamlit as st
import pandas as pd
import pickle


indian_cities = {
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
}

# ----------------- Load Trained Model -----------------
st.sidebar.header("⚙️ Model Status")

try:
    with open("model/wind_speed_model.pkl", "rb") as f:
        model = pickle.load(f)
    st.sidebar.success("Model loaded successfully ✅")
except FileNotFoundError:
    st.sidebar.error("Model file not found! Please check 'model/wind_speed_model.pkl'")
    st.stop()

# ----------------- Streamlit UI -----------------
st.title("🌬️ Wind Speed Prediction App")
st.write("Select a city or enter coordinates manually to predict wind speed:")

# ----------------- City Suggestion Dropdown -----------------
selected_city = st.selectbox("🏙️ Select Indian City (optional)", ["Select"] + list(indian_cities.keys()))

if selected_city != "Select":
    st.session_state["lat"] = indian_cities[selected_city][0]
    st.session_state["lon"] = indian_cities[selected_city][1]

# ----------------- Input Fields -----------------
lat = st.number_input("🌍 Latitude (°)", min_value=-90.0, max_value=90.0, value=st.session_state.get("lat", 00.0), step=0.1, key="lat_input")
lon = st.number_input("🌐 Longitude (°)", min_value=-180.0, max_value=180.0, value=st.session_state.get("lon", 00.0), step=0.1, key="lon_input")
altitude = st.number_input("🗻 Altitude (meters)", min_value=0.0, max_value=22000.0, value=0.0, step=100.0)
month = st.number_input("📅 Month (1-12)", min_value=1, max_value=12, value=7)
year = st.number_input("🗓️ Year", min_value=1948, max_value=2100, value=2025)

# ----------------- Prediction Button -----------------
if st.button("🔮 Predict Wind Speed"):
    
    input_data = pd.DataFrame({
        'lat': [lat],
        'lon': [lon],
        'altitude': [altitude],
        'month': [month],
        'year': [year]
    })

    try:
        wind_speed = model.predict(input_data)[0]

        st.success(f"🌪️ Predicted Wind Speed: **{wind_speed:.2f} m/s**")
        st.info(f"⚡ Equivalent Wind Speed: **{wind_speed * 3.6:.2f} km/h**")

    except Exception as e:
        st.error(f"Prediction failed: {e}")


st.sidebar.header("📊 Model Performance")

try:
    with open("model/metrics.txt", "r") as f:
        metrics = f.read()
    st.sidebar.text(metrics)
except FileNotFoundError:
    st.sidebar.warning("Model metrics file not found.")
