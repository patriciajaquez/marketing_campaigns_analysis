import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data_path = "/Users/patriciajaquez/Documents/GitHub/module1_project/data/processed/marketingcampaigns_clean.csv"
df = pd.read_csv(data_path)

# App title
st.title("Marketing Campaigns EDA")

# Sidebar filters
st.sidebar.header("Filters")
channel_filter = st.sidebar.multiselect("Select Channels", options=df['channel'].unique(), default=df['channel'].unique())
audience_filter = st.sidebar.multiselect("Select Audience", options=df['target_audience'].unique(), default=df['target_audience'].unique())

# Filter data
filtered_data = df[(df['channel'].isin(channel_filter)) & (df['target_audience'].isin(audience_filter))]

# Display filtered data
st.write("Filtered Data", filtered_data)

# Example visualization: ROI by channel
st.header("ROI by Channel")
fig, ax = plt.subplots()
sns.boxplot(x='channel', y='roi', data=filtered_data, ax=ax)
st.pyplot(fig)

# Add more sections for other questions