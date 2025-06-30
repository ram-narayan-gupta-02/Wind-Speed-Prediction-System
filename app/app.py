import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
MODEL_PATH = "model/wind_speed_model.pkl"
METRICS_PATH = "model/metrics.txt"

# Load model and metrics
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, 'r', encoding='latin1') as f:
            return f.read()
    else:
        return "No metrics found."

# Wind speed prediction
def predict_wind_speed(model, input_data):
    df = pd.DataFrame([input_data])
    prediction_knots = model.predict(df)[0]
    prediction_mps = prediction_knots * 0.514444
    prediction_kph = prediction_mps * 3.6
    return prediction_mps, prediction_kph


# --- Streamlit UI ---

# --- Title with Logo ---
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://cdn-icons-png.flaticon.com/512/1117/1117466.png' width='100'>
        <h1>🌬️ Wind Speed Prediction System</h1>    
        <p>Predict wind speed using different components — outputs in m/s and km/h</p>
    </div>
    <hr>
""", unsafe_allow_html=True)

# --- Input Form ---
with st.form("input_form"):
    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input("Latitude", format="%.4f")
        longitude = st.number_input("Longitude", format="%.4f")
        elevation = st.number_input("Elevation (meters)", format="%.2f")
        temp = st.number_input("Temperature (°C)")
        dewp = st.number_input("Dew Point (°C)")

    with col2:
        slp = st.number_input("Sea-Level Pressure (SLP)", format="%.2f")
        stp = st.number_input("Station Pressure (STP)", format="%.2f")
        mxspd = st.number_input("Max Wind Speed (MXSPD)", format="%.2f")
        gust = st.number_input("Gust Speed (GUST)", format="%.2f")

    submit = st.form_submit_button("Predict Wind Speed")

# --- Predict and Display ---
if submit:
    model = load_model()

    input_data = {
        'LATITUDE': latitude,
        'LONGITUDE': longitude,
        'ELEVATION': elevation,
        'TEMP': temp,
        'DEWP': dewp,
        'SLP': slp,
        'STP': stp,
        'MXSPD': mxspd,
        'GUST': gust
    }

    mps, kph = predict_wind_speed(model, input_data)

    st.success("✅ Prediction Complete!")
    st.metric(label="Wind Speed (m/s)", value=f"{mps:.2f}")
    st.metric(label="Wind Speed (km/h)", value=f"{kph:.2f}")

    # --- Chart Section
    st.subheader("📊 Wind Speed Visualization")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Bar Chart (m/s vs km/h)**")
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        units = ['m/s', 'km/h']
        values = [mps, kph]
        sns.barplot(x=units, y=values, palette='coolwarm', ax=ax1)
        ax1.set_ylabel("Speed")
        ax1.set_title("Predicted Wind Speed")
        st.pyplot(fig1)

    with col2:
        st.markdown("**Simulated Real vs Predicted Line Chart**")
        steps = list(range(1, 6))
        real = [mps + np.random.uniform(-0.5, 0.5) for _ in steps]
        predicted = [mps for _ in steps]

        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.plot(steps, real, label='Real', marker='o')
        ax2.plot(steps, predicted, label='Predicted', marker='x')
        ax2.set_title("Simulated Trend")
        ax2.set_xlabel("Steps")
        ax2.set_ylabel("Speed (m/s)")
        ax2.legend()
        st.pyplot(fig2)

    # --- Side-by-side: Feature Importance + Metrics ---
    col3, col4 = st.columns(2)

    with col3:
        if hasattr(model, "feature_importances_"):
            st.subheader("📌 Feature Importance")
            
            # Manually set features in correct order used during training
            features = ['LATITUDE', 'LONGITUDE', 'ELEVATION', 'TEMP', 'DEWP', 'SLP', 'STP', 'MXSPD', 'GUST']

            importances = model.feature_importances_

            # Sort for better visual
            importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
            importance_df = importance_df.sort_values(by='Importance', ascending=False)

            fig3, ax3 = plt.subplots(figsize=(5, 3))
            sns.barplot(data=importance_df, x='Importance', y='Feature', palette='crest', ax=ax3)
            ax3.set_title("Feature Importance")
            st.pyplot(fig3)  

    with col4:
        st.subheader("📄 Model Metrics")
        st.code(load_metrics())

# --- Footer ---
st.markdown("""
<hr>
<div style='text-align: center; padding: 10px; font-size: 15px;'>
    🛰️ Internship Project <b>@ ADRDE, DRDO</b>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
# st.markdown("Made by **Ram Narayan Gupta** | Internship Project @ DRDO ADRDE")
