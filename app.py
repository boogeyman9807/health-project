import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

#  Web App Title
st.title("HealthTech")

# Initialize session state for storing records
if "records" not in st.session_state:
    st.session_state["records"] = []

#  User Input Form
with st.form("health_form"):
    name = st.text_input("Enter your Name")
    age = st.number_input("Enter your Age", min_value=1, max_value=120, step=1)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Enter your Weight (kg)", min_value=1.0, step=0.5)
    height = st.number_input("Enter your Height (cm)", min_value=30.0, step=0.5)
    heart_rate = st.number_input("Enter your Heart Rate (bpm)", min_value=1, step=1)
    blood_pressure = st.number_input("Enter your Blood Pressure", min_value=1, step=1)
    sugar = st.number_input("Enter your Blood Sugar Level (mg/dL)", min_value=1, step=1)
    temperature = st.number_input("Enter your Body Temperature (°C)", min_value=20.0, step=0.1)
    pulse = st.number_input("Enter your Pulse Rate", min_value=1, step=1)

    submitted = st.form_submit_button("Check Health")

if submitted:
    st.subheader("📊 Health Insights")

    # ✅ BMI Calculation
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        bmi_status, bmi_score = "Underweight", 70
    elif 18.5 <= bmi < 24.9:
        bmi_status, bmi_score = "Normal", 100
    elif 25 <= bmi < 29.9:
        bmi_status, bmi_score = "Overweight", 70
    else:
        bmi_status, bmi_score = "Obese", 50
    st.write(f"**BMI:** {bmi:.2f} → {bmi_status}")

    # ✅ Heart Rate
    hr_status, hr_score = ("Normal", 100) if 60 <= heart_rate <= 100 else ("Abnormal", 50)
    st.write(f"**Heart Rate:** {heart_rate} → {hr_status}")

    # ✅ Blood Pressure
    bp_status, bp_score = ("Normal", 100) if 80 <= blood_pressure <= 120 else ("Abnormal", 50)
    st.write(f"**Blood Pressure:** {blood_pressure} → {bp_status}")

    # ✅ Sugar
    sugar_status, sugar_score = ("Normal", 100) if 70 <= sugar <= 140 else ("Abnormal", 50)
    st.write(f"**Sugar Level:** {sugar} → {sugar_status}")

    # ✅ Temperature
    temp_status, temp_score = ("Normal", 100) if temperature <= 37.5 else ("High (Possible Fever)", 50)
    st.write(f"**Temperature:** {temperature}°C → {temp_status}")

    # ✅ Pulse
    pulse_status, pulse_score = ("Normal", 100) if 60 <= pulse <= 100 else ("Abnormal", 50)
    st.write(f"**Pulse Rate:** {pulse} → {pulse_status}")

    # ✅ Final Health Score
    total_score = (bmi_score + hr_score + bp_score + sugar_score + temp_score + pulse_score) / 6
    if total_score >= 90:
        remark = "🌟 Excellent Health"
    elif total_score >= 75:
        remark = "👍 Good Health"
    elif total_score >= 60:
        remark = "⚠️ Needs Attention"
    else:
        remark = "🚨 Critical - Consult Doctor"

    st.success(f"**Final Health Score:** {total_score:.2f}/100 → {remark}")

    # ✅ Bar Chart
    labels = ['Heart Rate', 'Blood Pressure', 'Sugar', 'Temperature', 'Pulse', 'BMI', 'Health Score']
    values = [heart_rate, blood_pressure, sugar, temperature, pulse, bmi, total_score]
    colors = ['#66b3ff', '#99ff99', '#ffcc99', '#ff9999', '#c2c2f0', '#ffb366', '#66ff99']

    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(labels, values, color=colors)
    ax.set_title(f"Health Vitals & Score - {name} (Age: {age})")
    ax.set_ylabel("Values")
    plt.xticks(rotation=30)

    st.pyplot(fig)

    # ✅ Save Data with Date
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state["records"].append({
        "Date": current_time.split(" ")[0],
        "Time": current_time.split(" ")[1],
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Weight (kg)": weight,
        "Height (cm)": height,
        "BMI": round(bmi, 2),
        "Heart Rate": heart_rate,
        "Blood Pressure": blood_pressure,
        "Sugar": sugar,
        "Temperature (°C)": temperature,
        "Pulse": pulse,
        "Health Score": round(total_score, 2),
        "Remark": remark
    })

# ✅ Display Saved Records as Table
if st.session_state["records"]:
    st.subheader("📑 Health Records")
    df = pd.DataFrame(st.session_state["records"])
    st.dataframe(df, use_container_width=True)

    # ✅ Show summary per day
    st.subheader("📆 Daily Test Summary")
    daily_summary = df.groupby("Date").size().reset_index(name="Total Tests")
    st.table(daily_summary)


