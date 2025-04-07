import streamlit as st
from openai import OpenAI

import os


# In the title, include a muscle emoji for the fitness coach app
st.title(":muscle: Fitness Coach App")
st.markdown("This app creates a fitness program based on user goals.")

# Load API keys from .env file

#openai_api_key = os.getenv("OPENAI_API_KEY")

# Create a function that uses the OpenAI API to create a fitness program based on user goals
# It should create it based on the following:
# Gender, Age, Weight, Height, Fitness Goal, Days Available to Workout, Time of Day available to work out, Injuries, medical conditions,
# Motivation Level (self motivated, need a coach)
def create_fitness_program_openai(gender, age, weight, training_location,fitness_goals, days, time_of_day, injuries, medical_conditions, motivation_level, equipment_images,feet=0, inches=0, centimeters=0):
    """
    This function uses the OpenAI API to create a fitness program based on user goals,
    days, time of day available to workout, injuries, medical conditions, and motivation level.
    """
    client = OpenAI(api_key=openai_api_key)
    prompt = f'''
        You are a fitness coach. 
        Create a fitness program based on the following user information: 
        Gender: {gender}, Age: {age}, Weight: {weight}, 
        Height: If in feet {feet} and inches {inches} if those are greater than 0, else {centimeters} cm,
        Training location: {training_location},
        Equipment available: {equipment},
        Fitness Goals: {fitness_goals}, 
        Days available to workout: {days} , time of day available to workout: {time_of_day}, 
        injuries: {injuries}, medical conditions {medical_conditions}, and motivation level {motivation_level}. The fitness
        program should also include links to videos of the exercises, and a detailed description of each exercise. Note that
        if videos are not available in on one channel, you can use other channels like youtube, vimeo, or other video platforms.
        The program should include a warm-up and cool-down routine, and should be tailored to the user's fitness level.
        Also, the program should consider the pictures of the available equipment in the gym {equipment_images}.
        Additionally, generate a meal plan that has foods they should eat more of and foods they should eat less of or avoid.
        The meal plan should be based on the user's fitness goals and dietary preferences.
        '''
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content


# Create a user form that collects the following information:
# gender, age, weight (in lbs), height (ft and inches), fitness_goals, days, time_of_day, injuries, medical_conditions, motivation_level
st.write("Please fill out the form below to create a fitness program.")
feet = None
inches = None
centimeters = None
with st.container(border=True):
    st.write("Please enter your height:")
    height_unit = st.selectbox("Unit", ["Feet_inches", "Centimeters"], key="height_unit")
    # Dynamically display input fields based on the selected unit
    if st.session_state.height_unit == 'Feet_inches':
        feet = st.number_input("Feet", min_value=0, step=1)
        inches = st.number_input("Inches", min_value=0, max_value=11,step=1)
        #st.write(f"Height: {feet} feet, {inches} inches")
    else:
        centimeters = st.number_input("Centimeters", min_value=0.0, step=0.1)
        #st.write(f"Height: {centimeters} cm")

with st.container(border=True):
    st.write("Please select if you are working out at gym or home and enter equipment:")
    training_location = st.selectbox("Location", ["Home", "Gym"], key="training_location")
    # Dynamically display input fields based on the selected location
    if st.session_state.training_location == 'Home':
        equipment = st.text_input("Equipment available at home")
    else:
        equipment = st.text_input("Equipment available at gym")


with st.form("fitness_program_form"):
    openai_api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key", 
    type="password", 
    help="You can find your API key at https://platform.openai.com/account/api-keys"
)
    
    gender = st.selectbox("Gender Male or Female",["Male","Female"])
    age = st.number_input("Enter your age", value=None, format=None)
    weight = st.number_input("Enter your weight in lbs")
    fitness_goals = st.selectbox("Select your fitness goal", ["Cardio", "Muscle Building - Body builders", 
                                                              "Strength Building - Power Lifters","Body Toning - average Joe" ,
                                                              "Endurance Training - Athletes","Weight Loss"])
    days = st.number_input("Enter the number of days you want to workout", min_value=1, max_value=7)
    time_of_day = st.selectbox("Select the time of day you are available to workout", ["morning", "afternoon", "evening"])
    injuries = st.text_input("Enter the type of injuries you have")
    medical_conditions = st.text_input("Enter any medical conditions you have")
    motivation_level = st.selectbox("Select your motivation level", ["self motivated", "need a coach"])
    uploaded_files = st.file_uploader("Upload pictures of the equipment available in your gym", 
        type=["jpg", "png", "jpeg"],accept_multiple_files=True)


    submitted = st.form_submit_button("Submit")
    if submitted:
        fitness_program = create_fitness_program_openai(gender, age, weight, training_location,fitness_goals, days, time_of_day, injuries, medical_conditions, motivation_level,uploaded_files,feet, inches, centimeters)
        st.write("Fitness Program:")
        st.write(fitness_program)
