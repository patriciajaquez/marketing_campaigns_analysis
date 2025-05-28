import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Creative Color Palette ---
color_map = {
    "email": "#9b59b6",         # Amethyst
    "social media": "#16a085",  # Teal
    "webinar": "#f39c12",       # Orange
    "podcast": "#e67e22",       # Carrot
    "promotion": "#e84393",     # Pink Glamour
    "organic": "#00b894",       # Greenish
    "paid": "#fdcb6e",          # Sunflower
    "referral": "#0984e3",      # Blue
}

# --- Custom CSS for creative look ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e0c3fc 100%);
    }
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        color: #222;
    }
    /* Sidebar header and widget labels */
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6,
    .stSidebar label {
        color: #6c3483 !important;
        font-weight: bold;
        font-family: 'Montserrat', sans-serif;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        font-size: 1.15rem;
        color: #6c3483;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
    }
    /* Metrics */
    .stMetric {
        background: #fffbe7;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(200, 170, 255, 0.08);
    }
    /* Dataframe */
    .stDataFrame {
        background: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Marketing Campaigns EDA Dashboard",
    page_icon="🌈",
    layout="wide"
)

# --- Load Data ---
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv("data/processed/marketingcampaigns_clean.csv")
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🎨 Creative Campaign Filters")
channels = df['channel'].unique().tolist()
types = df['type'].unique().tolist()
audiences = df['target_audience'].unique().tolist()

selected_channel = st.sidebar.multiselect("Channel", options=channels, default=channels)
selected_type = st.sidebar.multiselect("Campaign Type", options=types, default=types)
selected_audience = st.sidebar.multiselect("Target Audience", options=audiences, default=audiences)
roi_range = st.sidebar.slider("ROI Range", float(df['roi'].min()), float(df['roi'].max()), (float(df['roi'].min()), float(df['roi'].max())))
revenue_range = st.sidebar.slider("Revenue Range", float(df['revenue'].min()), float(df['revenue'].max()), (float(df['revenue'].min()), float(df['revenue'].max())))
date_range = st.sidebar.date_input("Start Date Range", [df['start_date'].min(), df['start_date'].max()])

# --- Filter Data ---
filtered_df = df[
    (df['channel'].isin(selected_channel)) &
    (df['type'].isin(selected_type)) &
    (df['target_audience'].isin(selected_audience)) &
    (df['roi'].between(*roi_range)) &
    (df['revenue'].between(*revenue_range)) &
    (df['start_date'].dt.date.between(date_range[0], date_range[1]))
].copy()

# --- Dynamic Summary Text ---
st.title("🌈 Creative Marketing Campaigns EDA Dashboard")
st.markdown(
    f"""
    <div style='font-size:1.1rem; color:#6c3483; margin-bottom:1em; font-family:Montserrat, sans-serif;'>
        <b>{len(filtered_df):,}</b> campaigns selected.
        <b>Channels:</b> {', '.join(selected_channel)} |
        <b>Types:</b> {', '.join(selected_type)} |
        <b>Audience:</b> {', '.join(selected_audience)}<br>
        <b>ROI:</b> {roi_range[0]:.2f} to {roi_range[1]:.2f} |
        <b>Revenue:</b> ${revenue_range[0]:,.0f} to ${revenue_range[1]:,.0f} |
        <b>Date:</b> {date_range[0]} to {date_range[1]}
    </div>
    """, unsafe_allow_html=True
)

# --- Tabs ---
tabs = st.tabs([
    "📊 Overview",
    "📈 Channel & Type Analysis",
    "💰 ROI & Revenue",
    "👥 Audience & Conversion",
    "🗓️ Temporal Patterns",
    "📝 Insights & Recommendations"
])

# --- Tab 1: Overview ---
with tabs[0]:
    st.subheader("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Campaigns", len(filtered_df))
    col2.metric("Avg. ROI", f"{filtered_df['roi'].mean():.2f}")
    col3.metric("Avg. Revenue", f"${filtered_df['revenue'].mean():,.0f}")
    col4.metric("Avg. Conversion Rate", f"{filtered_df['conversion_rate'].mean():.2%}")

    st.markdown("#### Channel Distribution")
    fig_channel = px.histogram(
        filtered_df, x="channel", color="channel",
        color_discrete_map=color_map, text_auto=True,
        title="Campaigns by Channel"
    )
    st.plotly_chart(fig_channel, use_container_width=True)

    st.markdown("#### Campaign Type Distribution")
    fig_type = px.histogram(
        filtered_df, x="type", color="type",
        color_discrete_map=color_map, text_auto=True,
        title="Campaigns by Type"
    )
    st.plotly_chart(fig_type, use_container_width=True)

# --- Tab 2: Channel & Type Analysis ---
with tabs[1]:
    st.subheader("Channel & Type Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### ROI by Channel")
        fig_roi_channel = px.box(
            filtered_df, x="channel", y="roi", color="channel",
            color_discrete_map=color_map, points="all",
            title="ROI Distribution by Channel"
        )
        st.plotly_chart(fig_roi_channel, use_container_width=True)
    with col2:
        st.markdown("##### Revenue by Type")
        fig_rev_type = px.box(
            filtered_df, x="type", y="revenue", color="type",
            color_discrete_map=color_map, points="all",
            title="Revenue Distribution by Campaign Type"
        )
        st.plotly_chart(fig_rev_type, use_container_width=True)

    st.markdown("##### Conversion Rate by Channel & Type")
    fig_conv = px.bar(
        filtered_df.groupby(['channel', 'type'])['conversion_rate'].mean().reset_index(),
        x="channel", y="conversion_rate", color="type",
        color_discrete_map=color_map, barmode="group",
        title="Avg. Conversion Rate by Channel & Type"
    )
    st.plotly_chart(fig_conv, use_container_width=True)

# --- Tab 3: ROI & Revenue ---
with tabs[2]:
    st.subheader("ROI & Revenue Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### ROI Distribution")
        fig_roi = px.histogram(
            filtered_df, x="roi", nbins=30, color_discrete_sequence=["#1f77b4"],
            title="ROI Distribution"
        )
        st.plotly_chart(fig_roi, use_container_width=True)
    with col2:
        st.markdown("##### Revenue Distribution")
        fig_rev = px.histogram(
            filtered_df, x="revenue", nbins=30, color_discrete_sequence=["#2ca02c"],
            title="Revenue Distribution"
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    st.markdown("##### Budget vs Revenue")
    fig_scatter = px.scatter(
        filtered_df, x="budget", y="revenue", color="channel",
        color_discrete_map=color_map, size=filtered_df['roi'].abs(), hover_data=["campaign_name"],
        title="Budget vs Revenue by Channel"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Tab 4: Audience & Conversion ---
with tabs[3]:
    st.subheader("Audience & Conversion Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Conversion Rate by Audience")
        fig_conv_aud = px.box(
            filtered_df, x="target_audience", y="conversion_rate", color="target_audience",
            color_discrete_sequence=["#1f77b4", "#ff7f0e"],
            title="Conversion Rate by Audience"
        )
        st.plotly_chart(fig_conv_aud, use_container_width=True)
    with col2:
        st.markdown("##### ROI by Audience")
        fig_roi_aud = px.box(
            filtered_df, x="target_audience", y="roi", color="target_audience",
            color_discrete_sequence=["#1f77b4", "#ff7f0e"],
            title="ROI by Audience"
        )
        st.plotly_chart(fig_roi_aud, use_container_width=True)

    st.markdown("##### Top 10 Campaigns by Net Profit")
    top_campaigns = filtered_df.nlargest(10, "net_profit")
    fig_top = px.bar(
        top_campaigns, x="net_profit", y="campaign_name", orientation="h",
        color="channel", color_discrete_map=color_map,
        title="Top 10 Campaigns by Net Profit"
    )
    st.plotly_chart(fig_top, use_container_width=True)

# --- Tab 5: Temporal Patterns ---
with tabs[4]:
    st.subheader("Temporal & Seasonal Patterns")
    filtered_df['start_month'] = pd.to_datetime(filtered_df['start_date']).dt.month
    filtered_df['start_quarter'] = pd.to_datetime(filtered_df['start_date']).dt.quarter

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Average ROI by Month")
        roi_month = filtered_df.groupby('start_month')['roi'].mean().reset_index()
        fig_month = px.line(
            roi_month, x="start_month", y="roi", markers=True,
            title="Average ROI by Month", labels={"start_month": "Month", "roi": "Avg. ROI"}
        )
        st.plotly_chart(fig_month, use_container_width=True)
    with col2:
        st.markdown("##### Average Revenue by Quarter")
        rev_quarter = filtered_df.groupby('start_quarter')['revenue'].mean().reset_index()
        fig_quarter = px.line(
            rev_quarter, x="start_quarter", y="revenue", markers=True,
            title="Average Revenue by Quarter", labels={"start_quarter": "Quarter", "revenue": "Avg. Revenue"}
        )
        st.plotly_chart(fig_quarter, use_container_width=True)

    st.markdown("##### ROI Heatmap by Quarter and Channel")
    pivot = filtered_df.pivot_table(index='start_quarter', columns='channel', values='roi', aggfunc='mean')
    fig_heat = px.imshow(
        pivot, text_auto=True, color_continuous_scale="Blues",
        labels=dict(x="Channel", y="Quarter", color="Avg. ROI"),
        title="ROI by Quarter and Channel"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# --- Tab 6: Insights & Recommendations ---
with tabs[5]:
    st.subheader("Insights & Recommendations")
    st.markdown("""
    ### Key Insights
    - **Email campaigns** have the highest median ROI, while **social media** is the most used channel.
    - **Webinars** generate the highest average revenue; **emails** have the best conversion rates.
    - **Organic channels** consistently outperform paid and promotional channels in ROI.
    - **B2B campaigns** have higher median ROI; **B2C** have higher conversion rates.
    - **Seasonality:** Campaigns launched in Q2 and Q4 show higher ROI and revenue.
    - **High-performing campaigns** (ROI > 0.5 and revenue > $500,000) are mostly organic, email-based, and have moderate budgets.
    - **Longer campaigns** do not necessarily yield higher ROI.

    ### Recommendations
    1. **Prioritize email and organic campaigns** for higher ROI.
    2. **Focus on webinars for revenue** and emails for conversion rates.
    3. **Tailor campaigns:** B2B for ROI, B2C for conversion.
    4. **Optimize budget allocation** to maximize ROI and conversion.
    5. **Schedule major campaigns in Q2 and Q4** to leverage seasonal peaks.
    6. **Replicate traits of high-performing campaigns** (moderate budget, organic/email).
    """)

    st.markdown("---")
    st.markdown("#### Data Table (Filtered)")
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered Data (CSV)", data=csv, file_name="filtered_campaigns.csv", mime="text/csv")

# --- End ---