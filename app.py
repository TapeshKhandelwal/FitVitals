import streamlit as st
import google.generativeai as genai
import os
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
    st.set_page_config(page_title="Health Assessment Tool", layout="centered")
    st.title("Health Assessment Tool")
    
    # Collect user inputs for health metrics
    st.subheader("Enter Your Health Data")
    age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)
    sex = st.selectbox("Select your sex", options=["Male", "Female"])
    systolic_bp = st.number_input("Enter your systolic blood pressure (mm Hg)", min_value=0)
    diastolic_bp = st.number_input("Enter your diastolic blood pressure (mm Hg)", min_value=0)
    heart_rate = st.number_input("Enter your heart rate (bpm)", min_value=0)
    weight = st.number_input("Enter your weight (kg)", min_value=0.0, format="%.1f")
    height = st.number_input("Enter your height (cm)", min_value=0.0, format="%.1f")
    
    # Button to trigger health assessment
    submit = st.button("Assess Health")

    if submit:
        # Prepare the input prompt for the API
        input_prompt = (
            f"You are a professional healthcare advisor. Based on the provided health parameters, categorize the user's health "
            f"status into risk levels and provide a recommendation.\n\n"
            f"User's Health Parameters:\n"
            f"- Age: {age}\n"
            f"- Sex: {sex}\n"
            f"- Systolic Blood Pressure: {systolic_bp} mm Hg\n"
            f"- Diastolic Blood Pressure: {diastolic_bp} mm Hg\n"
            f"- Heart Rate: {heart_rate} bpm\n"
            f"- Weight: {weight} kg\n"
            f"- Height: {height} cm\n\n"
            f"### Health Status Categorization\n"
            f"Define the user's health status risk level based on the following criteria:\n"
            f"1. *BMI (Body Mass Index)*:\n"
            f"   - Low risk: 18.5 - 24.9\n"
            f"   - Moderate risk: 25 - 29.9\n"
            f"   - High risk: below 18.5 (underweight) or 30 and above (overweight/obese)\n\n"
            f"2. *Blood Pressure*:\n"
            f"   - Low risk: Systolic (90-120 mm Hg) and Diastolic (60-80 mm Hg)\n"
            f"   - Moderate risk: Systolic (121-139 mm Hg) or Diastolic (81-89 mm Hg)\n"
            f"   - High risk: Systolic (140 mm Hg or higher) or Diastolic (90 mm Hg or higher)\n\n"
            f"3. *Heart Rate*:\n"
            f"   - Low risk: Resting heart rate of 60-100 bpm\n"
            f"   - Moderate risk: Resting heart rate of 101-110 bpm\n"
            f"   - High risk: Resting heart rate above 110 bpm\n\n"
            f"### Response Format\n"
            f"Please categorize the user's health status as follows:\n"
            f"- *Risk Level (1: Low, 2: Moderate, 3: High)*: Provide a risk level based on an analysis of the user's BMI, blood pressure, and heart rate.\n"
            f"- *Recommendation*: Provide brief advice based on the categorized risk level.\n\n"
            f"### Example Response\n"
            f"Risk Level: 2 (Moderate)\n"
            f"Recommendation: 'Your blood pressure and BMI are slightly elevated. Consider regular monitoring and lifestyle changes. Consultation with a healthcare provider is recommended for personalized advice.'\n\n"
            f"Please analyze and provide a response following this format."
        )

        # Get AI response and display it
        response = get_gemini_response(input_prompt)
        
        st.header("Health Assessment Result")
        st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()
