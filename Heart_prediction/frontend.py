import streamlit as st # it is used for the Ui part in the python projects.

# Set up page config for a wider, more modern look
st.set_page_config(page_title="Heart Attack Predictor", page_icon="❤️", layout="wide")
import pandas as pd
import numpy as np
import joblib

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model=joblib.load(os.path.join(BASE_DIR, "KNN_Heart.pkl"))
scaler=joblib.load(os.path.join(BASE_DIR, "KNN_Heart_Scaler.pkl"))
column=joblib.load(os.path.join(BASE_DIR, "KNN_Heart_Columns.pkl"))

st.markdown("""
<style>
    /* Reduce top padding to fit everything on one page */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 0rem;
    }
    /* Custom button styling */
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        height: 50px;
        font-size: 18px;
        font-weight: 600;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        color: white;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #ff4b4b; margin-bottom: 0;'>❤️ Heart Attack Risk Predictor</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:#606060; margin-top: 0;'>Enter patient details to calculate the probability of a heart attack</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 👤 Personal Details")
    age = st.slider("Age", 18, 90, 50)
    sex = st.selectbox("Sex", ["Male", "Female"])
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["Yes", "No"])
    oldpeak = st.slider("Oldpeak (ST depression)", 0.0, 6.0, 2.0, 0.1)

with col2:
    st.markdown("### 🩺 Clinical Metrics")
    resting_bps = st.slider("Resting Blood Pressure", 90, 200, 120)
    cholesterol = st.slider("Cholesterol", 100, 600, 200)
    thalach = st.slider("Maximum Heart Rate", 60, 220, 150)
    st_slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])

with col3:
    st.markdown("### 🫀 ECG & Angina")
    chest_pain_type = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"])
    restecg = st.selectbox("Resting ECG Results", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
    exang = st.selectbox("Exercise Induced Angina", ["Yes", "No"])

col_btn, col_out = st.columns([1, 2])
with col_btn:
    predict_clicked = st.button("Calculate Risk")

if predict_clicked:
    input_data = pd.DataFrame({
        "Age": [age],
        "RestingBP": [resting_bps],
        "Cholesterol": [cholesterol],
        "FastingBS": [1 if fbs == "Yes" else 0],
        "MaxHR": [thalach],
        "Oldpeak": [oldpeak],
        "Sex_M": [1 if sex == "Male" else 0],
        "ChestPainType_ATA": [1 if chest_pain_type == "Atypical Angina" else 0],
        "ChestPainType_NAP": [1 if chest_pain_type == "Non-anginal Pain" else 0],
        "ChestPainType_TA": [1 if chest_pain_type == "Typical Angina" else 0],
        "RestingECG_Normal": [1 if restecg == "Normal" else 0],
        "RestingECG_ST": [1 if restecg == "ST-T Wave Abnormality" else 0],
        "ExerciseAngina_Y": [1 if exang == "Yes" else 0],
        "ST_Slope_Flat": [1 if st_slope == "Flat" else 0],
        "ST_Slope_Up": [1 if st_slope == "Upsloping" else 0]
    })
    
    # Ensure columns are in the exact order as expected by the model
    input_data = input_data[column]
    
    input_data_scaled=scaler.transform(input_data)
    prediction=model.predict(input_data_scaled)
    
    with col_out:
        if prediction[0]==1:
            st.error("Heart Attack Probability: High 🚨")
        else:
            st.success("Heart Attack Probability: Low ✅")