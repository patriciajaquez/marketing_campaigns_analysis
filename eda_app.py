import streamlit as st

import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Marketing Campaigns Analysis",
    page_icon="📊",
    layout="wide"
)

# Optional: Custom styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f9f9f9;
        color: #333333;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/marketingcampaigns_clean.csv")
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("📂 Filter Campaigns")
channels = df['channel'].unique()
types = df['type'].unique()
audiences = df['target_audience'].unique()

selected_channels = st.sidebar.multiselect("📡 Channel", channels, default=channels)
selected_types = st.sidebar.multiselect("🎯 Type", types, default=types)
selected_audiences = st.sidebar.multiselect("👥 Audience", audiences, default=audiences)

# Filtered DataFrame
filtered_df = df[
    (df['channel'].isin(selected_channels)) &
    (df['type'].isin(selected_types)) &
    (df['target_audience'].isin(selected_audiences))
]

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "📡 Channel & Type",
    "💰 ROI & Revenue",
    "🎯 Audience & Conversion",
    "📅 Temporal Patterns",
    "🔎 Insights"
])

# --- TAB 1: Overview ---
with tab1:
    st.header("📊 General Overview")
    st.write("Basic statistical summary of the selected campaigns:")
    st.dataframe(filtered_df.describe())

    st.write("📈 Total campaigns:", filtered_df.shape[0])
    st.write("🗓️ Campaign Period:", f"{filtered_df['start_date'].min().date()} to {filtered_df['end_date'].max().date()}")

# --- TAB 2: Channel & Type ---
with tab2:
    st.header("📡 Campaign Channel & Type Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig_channel = px.box(filtered_df, x="channel", y="ROI", title="ROI by Channel", color="channel")
        st.plotly_chart(fig_channel, use_container_width=True)

    with col2:
        fig_type = px.box(filtered_df, x="type", y="ROI", title="ROI by Type", color="type")
        st.plotly_chart(fig_type, use_container_width=True)

# --- TAB 3: ROI & Revenue ---
with tab3:
    st.header("💰 ROI & Revenue Performance")

    col1, col2 = st.columns(2)

    with col1:
        fig_roi = px.histogram(filtered_df, x="ROI", nbins=30, title="Distribution of ROI", color_discrete_sequence=["#636EFA"])
        st.plotly_chart(fig_roi, use_container_width=True)

    with col2:
        fig_revenue = px.histogram(filtered_df, x="revenue", nbins=30, title="Distribution of Revenue", color_discrete_sequence=["#EF553B"])
        st.plotly_chart(fig_revenue, use_container_width=True)

# --- TAB 4: Audience & Conversion ---
with tab4:
    st.header("🎯 Audience Targeting & Conversion")

    col1, col2 = st.columns(2)

    with col1:
        fig_audience_roi = px.box(filtered_df, x="target_audience", y="ROI", title="ROI by Target Audience", color="target_audience")
        st.plotly_chart(fig_audience_roi, use_container_width=True)

    with col2:
        fig_conversion = px.box(filtered_df, x="target_audience", y="conversion_rate", title="Conversion Rate by Audience", color="target_audience")
        st.plotly_chart(fig_conversion, use_container_width=True)

# --- TAB 5: Temporal Patterns ---
with tab5:
    st.header("📅 Time-Based Patterns")

    df['start_month'] = df['start_date'].dt.month_name()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    fig_month_roi = px.box(filtered_df, x="start_date", y="ROI", title="ROI Over Time")
    st.plotly_chart(fig_month_roi, use_container_width=True)

# --- TAB 6: Insights & Recommendations ---
with tab6:
    st.header("🔎 Final Insights & Recommendations")

    st.markdown("""
    ### 📌 Key Takeaways:
    - **Email campaigns** tend to yield the highest median ROI.
    - **Webinars** bring in the highest revenue on average.
    - **Organic channels** outperform paid ads in terms of ROI.
    - **B2B campaigns** generally show better ROI, while **B2C** has better conversion rates.
    - Campaigns launched in **Q2 and Q4** perform better overall.
    
    ### ✅ Recommendations:
    - Prioritize email and webinar campaigns for high ROI and revenue.
    - Consider shifting focus towards organic channels to reduce costs.
    - Use segmentation to tailor strategies for B2B vs B2C.
    - Launch major campaigns in Q2/Q4 to align with higher performance windows.
    """)

    st.download_button("📥 Download Filtered Data", filtered_df.to_csv(index=False), "filtered_data.csv")