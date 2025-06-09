import streamlit as st
import groq
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# Set page config with advanced theme
st.set_page_config(
    page_title="AI Fitness & Nutrition Planner",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with ultra-premium styling and animations
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Advanced Animations */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 201, 255, 0.4); }
        50% { transform: scale(1.05); box-shadow: 0 0 0 20px rgba(0, 201, 255, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 201, 255, 0); }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(0, 201, 255, 0.5), 0 0 10px rgba(0, 201, 255, 0.3); }
        50% { box-shadow: 0 0 20px rgba(0, 201, 255, 0.8), 0 0 30px rgba(0, 201, 255, 0.5); }
        100% { box-shadow: 0 0 5px rgba(0, 201, 255, 0.5), 0 0 10px rgba(0, 201, 255, 0.3); }
    }
    
    @keyframes slideIn {
        0% { transform: translateX(-100px) scale(0.9); opacity: 0; }
        100% { transform: translateX(0) scale(1); opacity: 1; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes rotate3D {
        0% { transform: perspective(1000px) rotateY(0deg); }
        100% { transform: perspective(1000px) rotateY(360deg); }
    }
    
    /* Enhanced Headers with 3D Effect */
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 50%, #00C9FF 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 201, 255, 0.3);
        position: relative;
        margin-bottom: 1.5rem;
        animation: float 6s ease-in-out infinite, shimmer 3s linear infinite;
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    h1::after, h2::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        border-radius: 3px;
        box-shadow: 0 0 10px rgba(0, 201, 255, 0.5);
        animation: glow 2s ease-in-out infinite;
    }
    
    /* Ultra-Premium Cards with 3D Effect */
    .stCard {
        background: rgba(26, 26, 46, 0.95) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        transform-style: preserve-3d !important;
        perspective: 1000px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stCard:hover {
        transform: translateY(-10px) rotateX(5deg) !important;
        box-shadow: 0 20px 40px rgba(0, 201, 255, 0.2) !important;
        border-color: rgba(0, 201, 255, 0.3) !important;
    }
    
    /* Premium Buttons with 3D Effect */
    .stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 20px rgba(0, 201, 255, 0.3) !important;
        transform-style: preserve-3d !important;
        perspective: 1000px !important;
        animation: pulse 2s infinite !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) rotateX(10deg) !important;
        box-shadow: 0 15px 30px rgba(0, 201, 255, 0.4) !important;
        animation: glow 2s infinite !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Premium Select Boxes with 3D Effect */
    .stSelectbox > div > div > select {
        background: rgba(26, 26, 46, 0.95) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2) !important;
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stSelectbox > div > div > select:hover {
        border-color: #00C9FF !important;
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.3) !important;
        transform: translateY(-3px) !important;
    }
    
    /* Premium Metrics with 3D Effect */
    .stMetric {
        background: rgba(26, 26, 46, 0.95) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stMetric:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 35px rgba(0, 201, 255, 0.2) !important;
        border-color: rgba(0, 201, 255, 0.3) !important;
    }
    
    /* Premium Tabs with 3D Effect */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem !important;
        background: rgba(26, 26, 46, 0.95) !important;
        padding: 1rem !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem !important;
        white-space: pre-wrap !important;
        background: transparent !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        padding: 0 1.5rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 20px rgba(0, 201, 255, 0.3) !important;
        transform: translateY(-3px) !important;
        animation: pulse 2s infinite !important;
    }
    
    /* Premium Messages with 3D Effect */
    .stAlert {
        background: rgba(26, 26, 46, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin: 1.5rem 0 !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Premium File Uploader with 3D Effect */
    .stFileUploader {
        background: rgba(26, 26, 46, 0.95) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stFileUploader:hover {
        border-color: #00C9FF !important;
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.3) !important;
        transform: translateY(-3px) !important;
    }
    
    /* Premium Spinner with 3D Effect */
    .stSpinner > div {
        border: 4px solid rgba(255, 255, 255, 0.1) !important;
        border-top: 4px solid #00C9FF !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        animation: spin 1s linear infinite, glow 2s infinite !important;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 12px !important;
        height: 12px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 6px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%) !important;
        border-radius: 6px !important;
        border: 3px solid rgba(26, 26, 46, 0.95) !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%) !important;
        box-shadow: 0 0 10px rgba(0, 201, 255, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("AI Fitness & Nutrition Planner")
    
    # Initialize session state
    if 'meal_plan' not in st.session_state:
        st.session_state.meal_plan = None
    
    # Sidebar for API key
    with st.sidebar:
        st.header("API Configuration")
        api_key = st.text_input("Enter your Groq API Key", type="password")
        
        if not api_key:
            st.warning("Please enter your Groq API key to continue")
            st.info("Get your API key from [Groq](https://console.groq.com)")
            return
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This app generates personalized fitness and nutrition plans using AI.
        Simply fill in your details and get a customized plan!
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Personal Information")
        
        # User input fields
        age = st.number_input("Age", min_value=15, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
        activity_level = st.selectbox(
            "Activity Level",
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
        )
        goal = st.selectbox(
            "Fitness Goal",
            ["Weight Loss", "Muscle Gain", "Maintenance", "General Fitness"]
        )
        
        # Generate plan button
        if st.button("Generate Plan", type="primary"):
            with st.spinner("Generating your personalized plan..."):
                user_data = {
                    "age": age,
                    "gender": gender,
                    "weight": weight,
                    "height": height,
                    "activity_level": activity_level,
                    "goal": goal
                }
                
                meal_plan = generate_meal_plan(user_data, api_key)
                if meal_plan:
                    st.session_state.meal_plan = meal_plan
                    st.success("Plan generated successfully!")
                else:
                    st.error("Failed to generate plan. Please check your API key and try again.")
    
    with col2:
        st.header("Your Plan")
        if st.session_state.meal_plan:
            st.markdown(st.session_state.meal_plan)
            
            # Download button
            if st.button("Download Plan"):
                download_plan(st.session_state.meal_plan)
        else:
            st.info("Fill in your details and generate a plan to see it here!")

def generate_meal_plan(user_data, api_key):
    """Generate a personalized meal plan using Groq."""
    try:
        # Initialize Groq client
        client = groq.Groq(api_key=api_key)
        
        # Create a detailed prompt for meal planning
        prompt = f"""
        Create a detailed 7-day meal plan for a {user_data['age']}-year-old {user_data['gender'].lower()} with the following characteristics:
        - Weight: {user_data['weight']} kg
        - Height: {user_data['height']} cm
        - Activity Level: {user_data['activity_level']}
        - Goal: {user_data['goal']}
        
        Please provide:
        1. Daily calorie target
        2. Macronutrient breakdown (protein, carbs, fats)
        3. 7-day meal plan with:
           - Breakfast
           - Morning Snack
           - Lunch
           - Afternoon Snack
           - Dinner
        4. Portion sizes
        5. Nutritional information for each meal
        6. Shopping list
        7. Meal prep tips
        
        Format the response in a clear, structured way.
        """
        
        # Generate the meal plan using llama3-70b-8192
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a professional nutritionist and fitness expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Error generating meal plan: {str(e)}")
        return None

def download_plan(plan_text):
    """Create a downloadable text file of the meal plan."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"meal_plan_{timestamp}.txt"
    
    # Create the download button
    st.download_button(
        label="Click to Download",
        data=plan_text,
        file_name=filename,
        mime="text/plain"
    )

if __name__ == "__main__":
    main()