
# 🌬️ Wind Speed Prediction System
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Live Demo:** [Wind Speed Prediction System 🚀](https://ram-narayan-gupta-02.github.io/Wind-Speed-Prediction-System/)  

---

## 📖 Overview

The **Wind Speed Prediction System** is a machine learning-powered platform designed to predict wind speed based on historical atmospheric data. 
![Wind Speed Prediction Model](wind-turbine.jpg)
This tool is particularly useful for applications in aerospace, research, and meteorology, providing wind speed forecasts, helping with safety assessments and planning.

---

## 🎯 Features

✅ Predict wind speed for different paramters
✅ Supports input in **m/s** and **km/h**  
✅ Provides output in both **m/s** and **km/h**  
✅ Visualizes trends with interactive charts  
✅ Displays model performance metrics like **Mean Squared Error (MSE)** and **R² Score**  
✅ Clean and responsive Streamlit-based web interface  

---

## 🛠️ Technology Stack

- **Python 3.13+**  
- **Streamlit** for interactive web UI  
- **scikit-learn** for machine learning  
- **Pandas, NumPy** for data handling  
- **Matplotlib, Seaborn** for data visualization  

---

## 🗂️ Project Structure

```
Wind-Speed-Prediction-System/
│
├── model/                      # Model training and prediction scripts
|   ├──metrics.txt       
|   ├──wind_speed_model.pkl
|   └──wind_speed_predictor.py             
├── app/                        # Streamlit front-end
|   └──app.py                   
├── README.md                   # Project documentation
└── requirements.txt            # Project dependencies
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ram-narayan-gupta-02/Wind-Speed-Prediction-System.git
cd Wind-Speed-Prediction-System
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit App

```bash
python -m streamlit run app/app.py
```

The app will open in your browser at **`http://localhost:8501`**.

---

## 📊 Model Details

The model utilizes historical atmospheric data with features like:

- Latitude & Longitude  
- Altitude, Year, Month, Day

**Output:** Predicted wind speed for valid inputs values.

---

## ⚡ Future Enhancements

- Incorporate real-time weather API support  
- Improve model accuracy with advanced algorithms  
- Deploy as a cloud-hosted application  

---

## 🙌 Acknowledgments

- **NOAA** for providing historical atmospheric data  
- **Scikit-learn & Streamlit** community for excellent open-source tools  

---

## 📩 Contact

**Ram Narayan Gupta**  
📧 [ramnrngupta@gmail.com](mailto:ramnrngupta@gmail.com)  
🌐 [LinkedIn Profile](https://www.linkedin.com/in/ram-narayan-gupta)  

---

**If you find this project useful, don't forget to ⭐ the repository!**
