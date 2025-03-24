import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "You may need to gain some weight for better health.", "blue"
    elif 18.5 <= bmi < 24.9:
        return "Normal Weight", "You have a healthy weight. Keep it up!", "green"
    elif 25 <= bmi < 29.9:
        return "Overweight", "You may need to lose some weight for better health.", "orange"
    else:
        return "Obese", "It's important to take steps to reduce your weight for better health.", "red"

def calculate_ideal_weight(height, gender):
    if gender == "Male":
        return 50 + 0.91 * (height * 100 - 152.4)
    else:
        return 45.5 + 0.91 * (height * 100 - 152.4)

def calculate_daily_calories(weight, height, age, gender, activity_level):
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * age)
    
    activity_multiplier = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    
    return bmr * activity_multiplier[activity_level]

st.set_page_config(page_title="BMI Calculator Pro", page_icon="📊", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stNumberInput>div>div>input {
        border-radius: 8px;
        padding: 10px;
    }
    .stMarkdown h1 {
        color: #4CAF50;
    }
    .stMarkdown h2 {
        color: #2E86C1;
    }
    .stMarkdown h3 {
        color: #D35400;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 BMI Calculator Pro")
st.write("""
Calculate your Body Mass Index (BMI) to understand your weight status. 
BMI is a simple calculation using a person's height and weight. The formula is BMI = kg/m² where kg is a person's weight in kilograms and m² is their height in meters squared.
""")

col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.1, format="%.1f")
with col2:
    height = st.number_input("Enter your height (m):", min_value=0.1, step=0.01, format="%.2f")

if st.button("Calculate BMI"):
    if weight > 0 and height > 0:
        bmi = calculate_bmi(weight, height)
        bmi_category, bmi_advice, bmi_color = interpret_bmi(bmi)
        
        st.success(f"Your BMI is: **{bmi:.2f}**")
        st.info(f"**Category:** {bmi_category}")
        st.write(f"**Advice:** {bmi_advice}")
        
        st.subheader("BMI Chart")
        st.image("https://www.cdc.gov/healthyweight/images/assessing/bmi-adult-fb-600x315.jpg", caption="BMI Categories", use_column_width=True)
        
        st.subheader("BMI Progress")
        bmi_min, bmi_max = 10, 40
        bmi_progress = max(0.0, min(1.0, (bmi - bmi_min) / (bmi_max - bmi_min)))  
        st.progress(bmi_progress)
        st.write(f"Your BMI is {bmi:.2f}, which is in the **{bmi_category}** range.")
        
        st.subheader("BMI Trend")
        bmi_trend = np.linspace(bmi_min, bmi_max, 100)
        category_colors = np.where(bmi_trend < 18.5, 'blue', np.where(bmi_trend < 24.9, 'green', np.where(bmi_trend < 29.9, 'orange', 'red')))
        
        fig, ax = plt.subplots()
        ax.bar(bmi_trend, np.ones_like(bmi_trend), color=category_colors, width=0.5)
        ax.axvline(x=bmi, color='black', linestyle='--', label='Your BMI')
        ax.set_xlabel("BMI")
        ax.set_ylabel("")
        ax.set_xticks(np.arange(bmi_min, bmi_max + 1, 5))
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Please enter valid weight and height values.")

st.sidebar.title("Additional Features")
st.sidebar.write("Explore more about your health:")

st.sidebar.subheader("Ideal Weight Calculator")
gender = st.sidebar.radio("Select your gender:", ("Male", "Female"))
age = st.sidebar.slider("Select your age:", 1, 100, 25)

if st.sidebar.button("Calculate Ideal Weight"):
    ideal_weight = calculate_ideal_weight(height, gender)
    st.sidebar.success(f"Your ideal weight is approximately **{ideal_weight:.1f} kg**.")

st.sidebar.subheader("Calorie Intake Calculator")
activity_level = st.sidebar.selectbox("Select your activity level:", 
                                      ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])

if st.sidebar.button("Calculate Daily Calorie Intake"):
    daily_calories = calculate_daily_calories(weight, height, age, gender, activity_level)
    st.sidebar.success(f"Your estimated daily calorie intake is **{daily_calories:.0f} kcal**.")

st.sidebar.subheader("Weight Loss/Gain Planner")
goal = st.sidebar.radio("Select your goal:", ("Lose Weight", "Gain Weight"))
target_weight = st.sidebar.number_input("Enter your target weight (kg):", min_value=1.0, step=0.1, format="%.1f")
weeks = st.sidebar.slider("Select the number of weeks to achieve your goal:", 1, 52, 12)

if st.sidebar.button("Calculate Plan"):
    weight_difference = target_weight - weight
    weekly_weight_change = weight_difference / weeks
    daily_calorie_change = weekly_weight_change * 7700 / 7  
    
    if goal == "Lose Weight":
        st.sidebar.success(f"To lose **{abs(weight_difference):.1f} kg** in **{weeks} weeks**, you need to reduce your daily calorie intake by **{abs(daily_calorie_change):.0f} kcal**.")
    else:
        st.sidebar.success(f"To gain **{abs(weight_difference):.1f} kg** in **{weeks} weeks**, you need to increase your daily calorie intake by **{abs(daily_calorie_change):.0f} kcal**.")

st.markdown("---")
st.write("Made with ❤️ by [Your Name]")