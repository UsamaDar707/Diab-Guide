import streamlit as st
import google.generativeai as genai

# Initialize Gemini API with the API key from Streamlit secrets
api_key = st.secrets["gemini_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to generate meal plan based on sugar levels using Gemini API
def generate_meal_plan_gemini(fasting, pre_meal, post_meal, diet_plan):
    prompt = f"""
    You are a diabetic meal planning assistant. Given the following inputs, generate a customized meal plan:
    - Fasting Sugar Level: {fasting} mg/dL
    - Pre-Meal Sugar Level: {pre_meal} mg/dL
    - Post-Meal Sugar Level: {post_meal} mg/dL
    - Dietary Plan: {diet_plan}

    Please provide a detailed meal plan suitable for the user's condition.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response.text else "No response received from the API."

# Caching function based on the input values
@st.cache_data
def cached_meal_plan(fasting, pre_meal, post_meal, diet_plan):
    return generate_meal_plan_gemini(fasting, pre_meal, post_meal, diet_plan)

# Streamlit App Layout
st.set_page_config(page_title="Diab-Guide", page_icon="🍏", layout="wide")

# Header
st.title("🍏 Diab-Guide: Personalized Diabetes Meal Planning")

# Description of the app with improved styling
st.markdown("""
Welcome to **Diab-Guide**, your go-to solution for managing diabetes with **tailored meal plans**. 🥗
Simply input your fasting, pre-meal, and post-meal sugar levels, along with your dietary preferences,
and receive a **customized meal plan** to help you maintain optimal sugar levels.
""", unsafe_allow_html=True)

# Create two columns for a more organized layout
col1, col2 = st.columns(2)

with col1:
    st.sidebar.header("Input Your Details")

    fasting_sugar = st.sidebar.number_input("Fasting Sugar Level (mg/dL)", min_value=0, key="fasting_sugar")
    pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Level (mg/dL)", min_value=0, key="pre_meal_sugar")
    post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Level (mg/dL)", min_value=0, key="post_meal_sugar")

with col2:
    diet_plan = st.sidebar.text_area("Current Dietary Plan", placeholder="e.g., vegetarian, vegan, keto", key="diet_plan")

# Add a button with an attractive style
button_style = """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
"""

st.markdown(button_style, unsafe_allow_html=True)

# Generate meal plan button
if st.sidebar.button("Generate Meal Plan"):
    if api_key:  # Ensure the API key is provided
        meal_plan = cached_meal_plan(fasting_sugar, pre_meal_sugar, post_meal_sugar, diet_plan)
        st.session_state.meal_plan = meal_plan  # Save the meal plan to session state
    else:
        st.write("🔑 API key is missing. Please check your Streamlit secrets.")

# Display the meal plan if it exists in session state
if 'meal_plan' in st.session_state:
    st.subheader("🍽️ Your Customized Meal Plan")
    st.write(st.session_state.meal_plan)
else:
    st.write("🔍 Please input your details in the sidebar and click 'Generate Meal Plan' to see the results.")
