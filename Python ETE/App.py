import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image, ImageEnhance
import base64

# Set Streamlit page config
st.set_page_config(page_title="Hackathon Analysis", layout="wide")

# Function to Set Background Image for Both Main Content and Sidebar
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    page_bg_img = f"""
    <style>
    .stApp, .stSidebar {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Call the function with your background image path
set_background("C:\\Users\\91766\\Desktop\\Python ETE\\background.jpg")  # Provide the correct path to your image

# Dark Theme Styling
st.markdown(
    """
    <style>
    .big-font { font-size:40px !important; font-weight: bold; text-align: center; }
    .medium-font { font-size:30px !important; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar description
st.sidebar.title("🚀 Hackathon Insights Dashboard")
st.sidebar.write(
    """
    - Welcome to the Hackathon Analysis Dashboard!
    - Gain deep insights into participant trends and feedback analysis.
    - Visualize data across various domains, states, and colleges.
    - Generate word clouds to analyze participant sentiments.
    - Upload and process images related to hackathon events.
    - Fully interactive and user-friendly with dark-themed aesthetics.
    - Supports 400 participants over 3 days in 5 hackathon domains.
    """
)

# Generate Dataset
def generate_data():
    domains = ['AI', 'Blockchain', 'Cybersecurity', 'IoT', 'FinTech']
    states = ['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Delhi', 'Telangana']
    colleges = [f'College {i}' for i in range(1, 11)]
    feedback_samples = ["Amazing experience!", "Challenging tasks.", "Loved the mentors!", "Networking was great.", "Could be better."]

    data = {
        'Participant_ID': [f'P{i}' for i in range(1, 401)],
        'Domain': [random.choice(domains) for _ in range(400)],
        'Day': [random.choice([1, 2, 3]) for _ in range(400)],
        'State': [random.choice(states) for _ in range(400)],
        'College': [random.choice(colleges) for _ in range(400)],
        'Feedback': [random.choice(feedback_samples) for _ in range(400)],
        'Age': np.random.randint(18, 30, 400),
        'Experience_Years': np.random.randint(0, 5, 400)
    }
    return pd.DataFrame(data)

df = generate_data()

# Sidebar Filters
st.sidebar.subheader("🔍 Filter Data")
selected_domain = st.sidebar.selectbox("Select Domain", ['All'] + sorted(df['Domain'].unique()))
selected_state = st.sidebar.selectbox("Select State", ['All'] + sorted(df['State'].unique()))
selected_college = st.sidebar.selectbox("Select College", ['All'] + sorted(df['College'].unique()))

filtered_df = df.copy()
if selected_domain != 'All':
    filtered_df = filtered_df[filtered_df['Domain'] == selected_domain]
if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['State'] == selected_state]
if selected_college != 'All':
    filtered_df = filtered_df[filtered_df['College'] == selected_college]

# Display Full Dataset
st.markdown("<h1 class='big-font'>📊 Hackathon Event - Data Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='medium-font'>📄 Filtered Dataset</h2>", unsafe_allow_html=True)
st.dataframe(filtered_df)

# Data Visualizations
st.markdown("<h2 class='medium-font'>📈 Data Visualizations</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

# Bar Chart - Participants per Domain
fig1 = px.bar(df, x='Domain', title="Participants per Domain", color='Domain')
col1.plotly_chart(fig1)

# Pie Chart - Participants per Day
fig2 = px.pie(df, names='Day', title="Participants per Day")
col2.plotly_chart(fig2)

# Histogram - Age Distribution
fig3 = px.histogram(df, x='Age', title="Age Distribution of Participants", nbins=10)
col3.plotly_chart(fig3)

# Scatter Plot - Age vs Experience
fig4 = px.scatter(df, x='Age', y='Experience_Years', title="Age vs Experience")
col4.plotly_chart(fig4)

# Bar Chart - Participants per State
fig5 = px.bar(df, x='State', title="Participants per State", color='State')
col5.plotly_chart(fig5)

# Histogram - Experience Distribution
fig6 = px.histogram(df, x='Experience_Years', title="Experience Level of Participants", nbins=5)
col6.plotly_chart(fig6)

# Text Analysis - Word Cloud
st.markdown("<h2 class='medium-font'>💬 Feedback Word Cloud</h2>", unsafe_allow_html=True)
feedback_text = " ".join(df['Feedback'])
wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='cool').generate(feedback_text)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# Image Upload & Processing
st.markdown("<h2 class='medium-font'>🖼️ Image Gallery & Processing</h2>", unsafe_allow_html=True)
uploaded_image = st.file_uploader("📤 Upload an Image", type=["jpg", "png", "jpeg"])
if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, caption="📷 Uploaded Image", use_container_width=True)

    # Custom Image Processing
    st.markdown("<h2 class='medium-font'>🎛️ Adjust Image Properties</h2>", unsafe_allow_html=True)
    bright_factor = st.slider("🌞 Brightness", 0.5, 2.0, 1.0)
    contrast_factor = st.slider("🎨 Contrast", 0.5, 2.0, 1.0)
    sharpness_factor = st.slider("🔍 Sharpness", 0.5, 2.0, 1.0)

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(bright_factor)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast_factor)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness_factor)

    st.image(img, caption="✨ Processed Image", use_container_width=True)