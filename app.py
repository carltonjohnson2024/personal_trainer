import streamlit as st
from openai import OpenAI

import os


# In the title, include a muscle emoji for the fitness coach app
st.title(":muscle: Fitness Coach App")
st.markdown("This app createsa fitness program based on user goals.")

# Load API keys from .env file

#openai_api_key = os.getenv("OPENAI_API_KEY")

# Create a function that uses the OpenAI API to create a fitness program based on user goals
# It should create it based on the following:
# Gender, Age, Weight, Height, Fitness Goal, Days Available to Workout, Time of Day available to work out, Injuries, medical conditions,
# Motivation Level (self motivated, need a coach)
def create_fitness_program_openai(gender, age, weight, height, fitness_goals, days, time_of_day, injuries, medical_conditions, motivation_level, equipment_images):
    """
    This function uses the OpenAI API to create a fitness program based on user goals,
    days, time of day available to workout, injuries, medical conditions, and motivation level.
    """
    client = OpenAI(api_key=openai_api_key)
    prompt = f'''
        You are a fitness coach. 
        Create a fitness program based on the following user information: 
        Gender: {gender}, Age: {age}, Weight: {weight}, Height: {height}, Fitness Goals: {fitness_goals}, 
        Days available to workout: {days} , time of day available to workout: {time_of_day}, 
        injuries: {injuries}, medical conditions {medical_conditions}, and motivation level {motivation_level}.
        Also, the program should consider the pictures of the available equipment in the gym {equipment_images}.
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
with st.form("fitness_program_form"):
    openai_api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key", 
    type="password", 
    help="You can find your API key at https://platform.openai.com/account/api-keys"
)
    gender = st.selectbox("Gender Male or Female",["Male","Female"])
    age = st.number_input("Enter your age", value=None, format=None)
    weight = st.number_input("Enter your weight in lbs")
    height = st.number_input("Enter your height in ft")
    fitness_goals = st.selectbox("Select your fitness goal", ["cardio", "muscle gain", "weight loss"])
    days = st.number_input("Enter the number of days you want to workout", min_value=1, max_value=7)
    time_of_day = st.selectbox("Select the time of day you are available to workout", ["morning", "afternoon", "evening"])
    injuries = st.text_input("Enter the type of injuries you have")
    medical_conditions = st.text_input("Enter any medical conditions you have")
    motivation_level = st.selectbox("Select your motivation level", ["self motivated", "need a coach"])
    uploaded_files = st.file_uploader("Upload pictures of the equipment available in your gym", 
        type=["jpg", "png", "jpeg"],accept_multiple_files=True)


    submitted = st.form_submit_button("Submit")
    if submitted:
        fitness_program = create_fitness_program_openai(gender, age, weight, height, fitness_goals, days, time_of_day, injuries, medical_conditions, motivation_level,uploaded_files)
        st.write("Fitness Program:")
        st.write(fitness_program)
