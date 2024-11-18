import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the response from the generative AI model
def get_gemini_response(input_prompt):
    """
    Interacts with the Gemini AI model to generate a response.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-exp-0801')
        response = model.generate_content([input_prompt])
        return response.text
    except Exception as e:
        return f"Error in generating response: {e}"

# Streamlit UI setup
def main():
    """
    Main function to run the Health Assessment Tool application.
    """
    # Page configuration
    st.set_page_config(page_title="FitVitals", layout="wide")

    # Apply custom CSS styles for better alignment and aesthetics
    st.markdown("""
    <style>
        .main-container {
            max-width: 1000px;
            margin: auto;
            padding: 10px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        .header-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }
        .subheader-title {
            font-size: 1.2em;
            color: #34495e;
            text-align: center;
        }
        .data-section {
            padding: 10px 20px;
        }
        .result-box {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            color: #333;
        }
        .custom-table {
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main container
    with st.container():
        st.markdown('<div class="main-container">', unsafe_allow_html=True)

        # Logo and Title
        st.image("FitVitalsLogo.jpg", width=250, use_column_width=False)
        st.markdown('<div class="header-title">FitVitals</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader-title">Your Daily Health Partner</div>', unsafe_allow_html=True)

        # Input section
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="data-section">', unsafe_allow_html=True)

        age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)
        sex = st.selectbox("Select your sex", options=["Male", "Female"])
        systolic_bp = st.number_input("Enter your systolic blood pressure (mm Hg)", min_value=0)
        diastolic_bp = st.number_input("Enter your diastolic blood pressure (mm Hg)", min_value=0)
        heart_rate = st.number_input("Enter your heart rate (bpm)", min_value=0)
        weight = st.number_input("Enter your weight (kg)", min_value=0.0, format="%.1f")
        height = st.number_input("Enter your height (cm)", min_value=0.0, format="%.1f")

        submit = st.button("Assess Health")

        # Calculate BMI if weight and height are provided
        bmi = weight / ((height / 100) ** 2) if height > 0 else None

        if submit:
            normal_values = {
                "Parameter": ["Age", "Sex", "Systolic BP (mm Hg)", "Diastolic BP (mm Hg)", "Heart Rate (bpm)", "Weight (kg)", "Height (cm)", "BMI"],
                "Normal Range": ["Varies", "Male/Female", "90-120", "60-80", "60-100", "Varies", "Varies", "18.5-24.9"],
                "Patient Value": [
                    age, sex, systolic_bp, diastolic_bp, heart_rate, weight, height, 
                    f"{bmi:.1f}" if bmi is not None else "N/A"
                ]
            }
            comparison_df = pd.DataFrame(normal_values)
            st.subheader("Comparison of Patient Values Against Normal Ranges")
            st.table(comparison_df.style.set_properties(**{'background-color': '#f9f9f9', 'border-color': 'black'}))

            input_prompt = f"""
            You are a professional healthcare advisor. Based on the provided health parameters, categorize the user's health status into risk levels and provide a recommendation.

            User's Health Parameters:
            - Age: {age}
            - Sex: {sex}
            - Systolic Blood Pressure: {systolic_bp} mm Hg
            - Diastolic Blood Pressure: {diastolic_bp} mm Hg
            - Heart Rate: {heart_rate} bpm
            - Weight: {weight} kg
            - Height: {height} cm
            - BMI: {f"{bmi:.1f}" if bmi is not None else "N/A"}

            ### Health Status Categorization
            1. *BMI*: Low risk: 18.5 - 24.9, Moderate: 25 - 29.9, High: <18.5 or >30
            2. *Blood Pressure*: Low risk: 90-120/60-80, Moderate: 121-139/81-89, High: 140+/90+
            3. *Heart Rate*: Low risk: 60-100 bpm, Moderate: 101-110 bpm, High: >110 bpm

            ### Format
            - *Risk Level*: (1: Low, 2: Moderate, 3: High)
            - *Recommendation*: Brief advice based on risk level.
            """
            response = get_gemini_response(input_prompt)

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.header("Health Assessment Result")
            st.markdown(
                f"""
                <h2>Health Status Analysis & Recommendation</h2>
                <p>{response}</p>
                """,
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
