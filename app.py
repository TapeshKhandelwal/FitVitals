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
    st.set_page_config(page_title="FitVitals", layout="centered")

    # Create two columns: left for the image, right for inputs
    col1, col2 = st.columns([1, 2])  # Adjust the proportions as needed

    # Left column: Display the logo image
    with col1:
        st.image("FitVitalsLogo.jpg", width=100, use_column_width=False)

    # Right column: Input fields and button
    with col2:
        st.title("FitVitals")
        st.subheader("Your Daily Health Partner")
        st.subheader("Enter Your Health Data")
        
        # Collect user inputs for health metrics
        age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)
        sex = st.selectbox("Select your sex", options=["Male", "Female"])
        systolic_bp = st.number_input("Enter your systolic blood pressure (mm Hg)", min_value=0)
        diastolic_bp = st.number_input("Enter your diastolic blood pressure (mm Hg)", min_value=0)
        heart_rate = st.number_input("Enter your heart rate (bpm)", min_value=0)
        weight = st.number_input("Enter your weight (kg)", min_value=0.0, format="%.1f")
        height = st.number_input("Enter your height (cm)", min_value=0.0, format="%.1f")

        # Button to trigger health assessment
        submit = st.button("Assess Health")

    # Calculate BMI if weight and height are provided
    bmi = weight / ((height / 100) ** 2) if height > 0 else None

    if submit:
        # Normal reference values
        normal_values = {
            "Parameter": ["Age", "Sex", "Systolic BP (mm Hg)", "Diastolic BP (mm Hg)", "Heart Rate (bpm)", "Weight (kg)", "Height (cm)", "BMI"],
            "Normal Range": ["Varies", "Male/Female", "90-120", "60-80", "60-100", "Varies", "Varies", "18.5-24.9"],
            "Patient Value": [
                age,
                sex,
                systolic_bp,
                diastolic_bp,
                heart_rate,
                weight,
                height,
                f"{bmi:.1f}" if bmi is not None else "N/A"
            ]
        }

        # Create a DataFrame for displaying comparison
        comparison_df = pd.DataFrame(normal_values)

        # Display comparison table below the assessment button
        st.subheader("Comparison of Patient Values Against Normal Ranges")
        st.table(comparison_df)

        # Prepare the input prompt for the API
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
        Define the user's health status risk level based on the following criteria:
        1. *BMI (Body Mass Index)*:
           - Low risk: 18.5 - 24.9
           - Moderate risk: 25 - 29.9
           - High risk: below 18.5 (underweight) or 30 and above (overweight/obese)

        2. *Blood Pressure*:
           - Low risk: Systolic (90-120 mm Hg) and Diastolic (60-80 mm Hg)
           - Moderate risk: Systolic (121-139 mm Hg) or Diastolic (81-89 mm Hg)
           - High risk: Systolic (140 mm Hg or higher) or Diastolic (90 mm Hg or higher)

        3. *Heart Rate*:
           - Low risk: Resting heart rate of 60-100 bpm
           - Moderate risk: Resting heart rate of 101-110 bpm
           - High risk: Resting heart rate above 110 bpm

        ### Response Format
        Please categorize the user's health status as follows:
        - *Risk Level (1: Low, 2: Moderate, 3: High)*: Provide a risk level based on an analysis of the user's BMI, blood pressure, and heart rate.
        - *Recommendation*: Provide brief advice based on the categorized risk level.

        ### Example Response
        Risk Level: 2 (Moderate)
        Recommendation: "Your blood pressure and BMI are slightly elevated. Consider regular monitoring and lifestyle changes. Consultation with a healthcare provider is recommended for personalized advice."

        Please analyze and provide a response following this format.
        """

        # Get AI response
        response = get_gemini_response(input_prompt)

        # Display the formatted response
        st.header("Health Assessment Result")
        st.markdown(
            f"""
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; color: #333;">
                <h2>Health Status Analysis & Recommendation</h2>
                <h3>Rationale:</h3>
                <ul>
                    <li><strong>BMI:</strong> Calculated and analyzed.</li>
                    <li><strong>Blood Pressure:</strong> Systolic and diastolic values evaluated.</li>
                    <li><strong>Heart Rate:</strong> Heart rate assessed.</li>
                </ul>
                <h3>Recommendation:</h3>
                <p>{response}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Run the Streamlit app
if __name__ == "__main__":
    main()
