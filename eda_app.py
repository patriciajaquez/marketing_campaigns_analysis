import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Marketing Campaigns EDA Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- Professional, Clean CSS ---
st.markdown("""
    <style>
    .stApp { background: #f9f9fb; }
    section[data-testid="stSidebar"] {
        background: #ffffff;
        color: #222;
        border-right: 1px solid #e3e6ea;
    }
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6,
    .stSidebar label {
        color: #1a2634 !important;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
    }
    .stMultiSelect, .stSelectbox, .stSlider, .stDateInput {
        background: #f5f6fa !important;
        border-radius: 6px !important;
        border: 1px solid #e3e6ea !important;
    }
    .stSlider > div[data-baseweb="slider"] > div {
        background: #f5f6fa !important;
    }
    .stSlider .rc-slider-handle {
        border-color: #888 !important;
        background: #888 !important;
    }
    .stSlider .rc-slider-track {
        background: #888 !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.12rem;
        color: #1a2634;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
    }
    .stMetric {
        background: #f5f6fa;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(44, 62, 80, 0.06);
    }
    .stDataFrame {
        background: #f9f9fb;
    }
    </style>
""", unsafe_allow_html=True
)

# --- Color Map for Channels ---
color_map = {
    "email": "#1976d2",
    "social media": "#26a69a",
    "webinar": "#f9a825",
    "podcast": "#8e24aa",
    "promotion": "#ef5350",
    "organic": "#388e3c",
    "paid": "#ffa726",
    "referral": "#42a5f5",
}

# --- Load Data ---
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv("data/processed/marketingcampaigns_clean.csv")
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("📊 Campaign Filters")
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
st.title("📈 Marketing Campaigns EDA Dashboard")
st.markdown(
    f"""
    <div style='font-size:1.1rem; color:#222; margin-bottom:1em; font-family:Montserrat, sans-serif;'>
        <b>{len(filtered_df):,}</b> CAMPAIGNS SELECTED.<br>
        <b>CHANNELS:</b> {', '.join([channel.capitalize() for channel in selected_channel])} |
        <b>TYPES:</b> {', '.join([campaign_type.capitalize() for campaign_type in selected_type])} |
        <b>AUDIENCE:</b> {', '.join([audience.upper() for audience in selected_audience])}<br>
        <b>ROI:</b> {roi_range[0]:.2f} TO {roi_range[1]:.2f} |
        <b>REVENUE:</b> ${revenue_range[0]:,.2f} TO ${revenue_range[1]:,.2f} |
        <b>DATE:</b> {date_range[0]} TO {date_range[1]}
    </div>
    """, unsafe_allow_html=True
)

# --- Tab 1: Overview ---
with tabs[0]:
    st.info("**General Overview Of The Filtered Dataset: Shows Key Metrics And The Distribution Of Campaigns By Channel And Type.**")
    st.subheader("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Campaigns", f"{len(filtered_df):,}")
    col2.metric("Avg. ROI", f"{filtered_df['roi'].mean():.2f}")
    col3.metric("Avg. Revenue", f"${filtered_df['revenue'].mean():,.2f}")
    col4.metric("Avg. Conversion Rate", f"{filtered_df['conversion_rate'].mean():.2%}")

    st.markdown("#### Channel Distribution")
    channel_counts = filtered_df['channel'].value_counts().reset_index()
    channel_counts.columns = ['channel', 'count']  # Rename columns for clarity
    fig_channel = px.bar(
        channel_counts,
        x='channel',  # Correct column name
        y='count',    # Correct column name
        color='channel',
        title="Number Of Campaigns By Channel",
        labels={'channel': 'Channel', 'count': 'Number Of Campaigns'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_channel, use_container_width=True)

    st.markdown("#### Campaign Type Distribution")
    type_counts = filtered_df['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']  # Rename columns for clarity
    fig_type = px.bar(
        type_counts,
        x='type',  # Correct column name
        y='count',  # Correct column name
        color='type',
        title="Number Of Campaigns By Type",
        labels={'type': 'Campaign Type', 'count': 'Number Of Campaigns'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_type, use_container_width=True)

# --- Tab 2: Channel & Type Analysis ---
with tabs[1]:
    st.info("**Compare The Performance Of Channels And Campaign Types In Terms Of ROI, Revenue, And Conversion Rate.**")
    st.subheader("Channel & Type Performance")

    # Most Frequently Used Channel and Best ROI
    st.markdown("#### Most Frequently Used Channel And Best ROI")
    channel_summary = filtered_df.groupby('channel').agg(
        total_campaigns=('channel', 'count'),
        avg_roi=('roi', 'mean')
    ).sort_values(by='total_campaigns', ascending=False).reset_index()
    channel_summary['avg_roi'] = channel_summary['avg_roi'].round(2)  # Format ROI
    st.dataframe(channel_summary.head(5), use_container_width=True)

    # Campaign Type with Most Revenue and Best Conversion Rate
    st.markdown("#### Campaign Type With Most Revenue And Best Conversion Rate")
    type_summary = filtered_df.groupby('type').agg(
        total_revenue=('revenue', 'sum'),
        avg_conversion_rate=('conversion_rate', 'mean')
    ).sort_values(by='total_revenue', ascending=False).reset_index()
    type_summary['total_revenue'] = type_summary['total_revenue'].apply(lambda x: f"${x:,.2f}")  # Format revenue
    type_summary['avg_conversion_rate'] = type_summary['avg_conversion_rate'].apply(lambda x: f"{x:.2%}")  # Format conversion rate
    st.dataframe(type_summary.head(5), use_container_width=True)

# --- Tab 3: ROI & Revenue ---
with tabs[2]:
    st.info("**Analyze The Distribution Of ROI And Revenue, And The Relationship Between Budget And Revenue.**")
    st.subheader("ROI & Revenue Analysis")

    # ROI Distribution
    st.markdown("#### ROI Distribution")
    fig_roi = px.box(
        filtered_df, y="roi", points="all", color_discrete_sequence=["#1976d2"],
        title="ROI Distribution", labels={"roi": "Return On Investment (ROI)"}
    )
    st.plotly_chart(fig_roi, use_container_width=True)

    # Revenue Distribution
    st.markdown("#### Revenue Distribution")
    fig_rev = px.box(
        filtered_df, y="revenue", points="all", color_discrete_sequence=["#26a69a"],
        title="Revenue Distribution", labels={"revenue": "Revenue"}
    )
    st.plotly_chart(fig_rev, use_container_width=True)

    # Budget vs Revenue Correlation
    st.markdown("#### Budget Vs Revenue Correlation")
    fig_corr = px.scatter(
        filtered_df, x="budget", y="revenue", color="channel",
        title="Budget Vs Revenue By Channel",
        labels={"budget": "Budget", "revenue": "Revenue"},
        color_discrete_map=color_map
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# --- Tab 4: Audience & Conversion ---
with tabs[3]:
    st.info("**Compare The Performance Between B2B And B2C Audiences, And Display The Most Profitable Campaigns.**")
    st.subheader("Audience & Conversion Analysis")

    # Conversion Rate by Audience
    st.markdown("#### Conversion Rate By Audience")
    audience_summary = filtered_df.groupby('target_audience').agg(
        avg_conversion_rate=('conversion_rate', 'mean'),
        total_campaigns=('target_audience', 'count')
    ).reset_index()
    audience_summary['avg_conversion_rate'] = audience_summary['avg_conversion_rate'].apply(lambda x: f"{x:.2%}")  # Format conversion rate
    st.dataframe(audience_summary, use_container_width=True)

    # Top 10 Campaigns by Net Profit
    st.markdown("#### Top 10 Campaigns By Net Profit")
    top_campaigns = filtered_df.nlargest(10, "net_profit")[['campaign_name', 'net_profit', 'channel', 'type']]
    top_campaigns['net_profit'] = top_campaigns['net_profit'].apply(lambda x: f"${x:,.2f}")  # Format net profit
    st.dataframe(top_campaigns, use_container_width=True)

# --- Tab 5: Temporal Patterns ---
with tabs[4]:
    st.info("**Explore Temporal And Seasonal Patterns In Campaign Performance.**")
    st.subheader("Temporal & Seasonal Patterns")

    # ROI by Month
    st.markdown("#### ROI By Month")
    filtered_df['start_month'] = filtered_df['start_date'].dt.month
    roi_month = filtered_df.groupby('start_month')['roi'].mean().reset_index()
    roi_month['roi'] = roi_month['roi'].round(2)  # Format ROI
    fig_month = px.line(
        roi_month, x="start_month", y="roi", markers=True,
        title="Average ROI By Month", labels={"start_month": "Month", "roi": "Avg. ROI"}
    )
    st.plotly_chart(fig_month, use_container_width=True)

    # Revenue by Quarter
    st.markdown("#### Revenue By Quarter")
    filtered_df['start_quarter'] = filtered_df['start_date'].dt.quarter
    rev_quarter = filtered_df.groupby('start_quarter')['revenue'].mean().reset_index()
    rev_quarter['revenue'] = rev_quarter['revenue'].apply(lambda x: f"${x:,.2f}")  # Format revenue
    fig_quarter = px.bar(
        rev_quarter, x="start_quarter", y="revenue", color="start_quarter",
        title="Average Revenue By Quarter", labels={"start_quarter": "Quarter", "revenue": "Avg. Revenue"}
    )
    st.plotly_chart(fig_quarter, use_container_width=True)

# --- Tab 6: Insights & Recommendations ---
with tabs[5]:
    st.info("**Summary of key findings and actionable recommendations based on the analysis.**")
    st.subheader("Insights & Recommendations")
    st.markdown("""
    ### Key Insights
    1. **Most Frequently Used Channel:** Promotion is the most frequently used channel.
    2. **Best ROI Channel:** Organic campaigns have the highest average ROI.
    3. **Top Campaign Type:** Social media campaigns generate the most revenue, while webinars have the best conversion rates.
    4. **B2B vs B2C:** Conversion rates are similar between B2B and B2C audiences.
    5. **Top Campaign:** The campaign with the highest net profit is "Advanced Systematic Complexity."
    6. **Budget vs Revenue:** There is a positive correlation between budget and revenue, but it varies by channel.
    7. **High-Performance Campaigns:** 534 campaigns have ROI > 0.5 and revenue > $500,000.
    8. **Seasonal Patterns:** ROI peaks in Q1 and Q4, while revenue peaks in Q2 and Q3.

    ### Recommendations
    - Focus on organic and promotion channels for higher ROI.
    - Prioritize social media and webinar campaigns for revenue and conversion rates.
    - Leverage seasonal trends by scheduling campaigns in Q1 and Q4.
    - Replicate characteristics of high-performing campaigns.
    """)