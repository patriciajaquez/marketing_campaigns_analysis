import streamlit as st
import pandas as pd
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
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['End Date'] = pd.to_datetime(df['End Date'])
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("📊 Campaign Filters")
channels = df['Channel'].unique().tolist()
types = df['Type'].unique().tolist()
audiences = df['Target Audience'].unique().tolist()

selected_channel = st.sidebar.multiselect("Channel", options=channels, default=channels)
selected_type = st.sidebar.multiselect("Campaign Type", options=types, default=types)
selected_audience = st.sidebar.multiselect("Target Audience", options=audiences, default=audiences)
roi_range = st.sidebar.slider("ROI Range", float(df['ROI'].min()), float(df['ROI'].max()), (float(df['ROI'].min()), float(df['ROI'].max())))
revenue_range = st.sidebar.slider("Revenue Range", float(df['Revenue'].min()), float(df['Revenue'].max()), (float(df['Revenue'].min()), float(df['Revenue'].max())))
date_range = st.sidebar.date_input("Start Date Range", [df['Start Date'].min(), df['Start Date'].max()])

# --- Filter Data ---
filtered_df = df[
    (df['Channel'].isin(selected_channel)) &
    (df['Type'].isin(selected_type)) &
    (df['Target Audience'].isin(selected_audience)) &
    (df['ROI'].between(*roi_range)) &
    (df['Revenue'].between(*revenue_range)) &
    (df['Start Date'].dt.date.between(date_range[0], date_range[1]))
].copy()

# --- Helper formatting functions ---
def format_money(x):
    return f"${x:,.2f}"

def format_percent(x):
    return f"{x:.2%}"

def format_number(x):
    return f"{x:,.0f}"

# --- Dynamic Summary Text ---
st.title("📈 Marketing Campaigns EDA Dashboard")
st.markdown(
    f"""
    <div style='font-size:1.1rem; color:#222; margin-bottom:1em; font-family:Montserrat, sans-serif;'>
        <b>{len(filtered_df):,}</b> campaigns selected.
        <b>Channels:</b> {', '.join(selected_channel)} |
        <b>Types:</b> {', '.join(selected_type)} |
        <b>Audience:</b> {', '.join(selected_audience)}<br>
        <b>ROI:</b> {roi_range[0]:.2f} to {roi_range[1]:.2f} |
        <b>Revenue:</b> ${revenue_range[0]:,.2f} to ${revenue_range[1]:,.2f} |
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
    st.info("**General overview of the filtered dataset: shows key metrics and the distribution of campaigns by channel and type.**")
    st.subheader("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Campaigns", f"{len(filtered_df):,}")
    col2.metric("Avg. ROI", f"{filtered_df['ROI'].mean():.2f}")
    col3.metric("Avg. Revenue", format_money(filtered_df['Revenue'].mean()))
    col4.metric("Avg. Conversion Rate", format_percent(filtered_df['Conversion Rate'].mean()))

    st.markdown("#### Channel Distribution")
    channel_counts = filtered_df['Channel'].value_counts().reset_index()
    channel_counts.columns = ['Channel', 'count']
    fig_channel = px.bar(
        channel_counts,
        x='Channel',
        y='count',
        color='Channel',
        title="Number of Campaigns by Channel",
        labels={'Channel': 'Channel', 'count': 'Number of Campaigns'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_channel, use_container_width=True)

    st.markdown("#### Campaign Type Distribution")
    type_counts = filtered_df['Type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'count']
    fig_type = px.bar(
        type_counts,
        x='Type',
        y='count',
        color='Type',
        title="Number of Campaigns by Type",
        labels={'Type': 'Campaign Type', 'count': 'Number of Campaigns'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_type, use_container_width=True)

# --- Tab 2: Channel & Type Analysis ---
with tabs[1]:
    st.info("**Compare the performance of channels and campaign types in terms of ROI, revenue, and conversion rate.**")
    st.subheader("Channel & Type Performance")

    # Most Frequently Used Channel and Best ROI
    st.markdown("#### Most Frequently Used Channel and Best ROI")
    channel_summary = filtered_df.groupby('Channel').agg(
        total_campaigns=('Channel', 'count'),
        avg_roi=('ROI', 'mean')
    ).sort_values(by='total_campaigns', ascending=False).reset_index()
    channel_summary['total_campaigns'] = channel_summary['total_campaigns'].map(format_number)
    channel_summary['avg_roi'] = channel_summary['avg_roi'].map(lambda x: f"{x:.2f}")
    st.dataframe(channel_summary.head(5), use_container_width=True)

    # Campaign Type with Most Revenue and Best Conversion Rate
    st.markdown("#### Campaign Type with Most Revenue and Best Conversion Rate")
    type_summary = filtered_df.groupby('Type').agg(
        total_revenue=('Revenue', 'sum'),
        avg_conversion_rate=('Conversion Rate', 'mean')
    ).sort_values(by='total_revenue', ascending=False).reset_index()
    type_summary['total_revenue'] = type_summary['total_revenue'].map(format_money)
    type_summary['avg_conversion_rate'] = type_summary['avg_conversion_rate'].map(format_percent)
    st.dataframe(type_summary.head(5), use_container_width=True)

    # --- Top Campaigns by Channel ---
    st.markdown("#### Top 5 Campaigns by Channel")
    top_by_channel = filtered_df.loc[filtered_df.groupby('Channel')['Net Profit'].idxmax()][
        ['Campaign Name', 'Net Profit', 'Channel', 'Type']
    ].sort_values(by='Net Profit', ascending=False)
    top_by_channel['Net Profit'] = top_by_channel['Net Profit'].map(format_money)
    st.dataframe(top_by_channel.head(5), use_container_width=True)

    # --- Top Campaigns by Type ---
    st.markdown("#### Top 5 Campaigns by Type")
    top_by_type = filtered_df.loc[filtered_df.groupby('Type')['Net Profit'].idxmax()][
        ['Campaign Name', 'Net Profit', 'Channel', 'Type']
    ].sort_values(by='Net Profit', ascending=False)
    top_by_type['Net Profit'] = top_by_type['Net Profit'].map(format_money)
    st.dataframe(top_by_type.head(5), use_container_width=True)

# --- Tab 3: ROI & Revenue ---
with tabs[2]:
    st.info("**Analyze the distribution of ROI and revenue, and the relationship between budget and revenue.**")
    st.subheader("ROI & Revenue Analysis")

    # ROI Distribution
    st.markdown("#### ROI Distribution")
    fig_roi = px.box(
        filtered_df, y="ROI", points="all", color_discrete_sequence=["#1976d2"],
        title="ROI Distribution", labels={"ROI": "Return on Investment (ROI)"}
    )
    fig_roi.update_yaxes(tickformat=".2f")
    st.plotly_chart(fig_roi, use_container_width=True)

    # Revenue Distribution
    st.markdown("#### Revenue Distribution")
    fig_rev = px.box(
        filtered_df, y="Revenue", points="all", color_discrete_sequence=["#26a69a"],
        title="Revenue Distribution", labels={"Revenue": "Revenue"}
    )
    fig_rev.update_yaxes(tickprefix="$", separatethousands=True, tickformat=".2f")
    st.plotly_chart(fig_rev, use_container_width=True)

    # Budget vs Revenue Correlation
    st.markdown("#### Budget vs Revenue Correlation")
    fig_corr = px.scatter(
        filtered_df, x="Budget", y="Revenue", color="Channel",
        title="Budget vs Revenue by Channel",
        labels={"Budget": "Budget", "Revenue": "Revenue"},
        color_discrete_map=color_map
    )
    fig_corr.update_xaxes(tickprefix="$", separatethousands=True, tickformat=".2f")
    fig_corr.update_yaxes(tickprefix="$", separatethousands=True, tickformat=".2f")
    st.plotly_chart(fig_corr, use_container_width=True)

    # Campaigns with High ROI and Revenue
    st.markdown("#### Campaigns with High ROI and Revenue")
    high_performance = filtered_df[(filtered_df['ROI'] > 0.5) & (filtered_df['Revenue'] > 500000)]
    high_performance_summary = high_performance[['Campaign Name', 'ROI', 'Revenue', 'Channel', 'Type']].copy()
    high_performance_summary['ROI'] = high_performance_summary['ROI'].map(lambda x: f"{x:.2f}")
    high_performance_summary['Revenue'] = high_performance_summary['Revenue'].map(format_money)
    st.dataframe(high_performance_summary, use_container_width=True)

with tabs[3]:
    st.info("**Compare the performance between B2B and B2C audiences, and display the most profitable campaigns.**")
    st.subheader("Audience & Conversion Analysis")

    # Conversion Rate by Audience
    st.markdown("#### Conversion Rate by Audience")
    audience_summary = filtered_df.groupby('Target Audience').agg(
        avg_conversion_rate=('Conversion Rate', 'mean'),
        total_campaigns=('Target Audience', 'count')
    ).reset_index()
    audience_summary['avg_conversion_rate'] = audience_summary['avg_conversion_rate'].map(format_percent)
    audience_summary['total_campaigns'] = audience_summary['total_campaigns'].map(format_number)
    st.dataframe(audience_summary, use_container_width=True)
    
    # Conversion Rate by Channel and Audience
    audience_channel = filtered_df.groupby(['Channel', 'Target Audience'])['Conversion Rate'].mean().reset_index()
    fig_aud_chan = px.bar(
        audience_channel,
        x='Channel',
        y='Conversion Rate',
        color='Target Audience',
        barmode='group',
        title="Conversion Rate by Channel and Audience"
    )
    fig_aud_chan.update_yaxes(tickformat=".2%")
    st.plotly_chart(fig_aud_chan, use_container_width=True)

    # Audience Conversion Rate by Type
    st.markdown("#### Audience Conversion Rate by Campaign Type")
    audience_type = filtered_df.groupby(['Type', 'Target Audience'])['Conversion Rate'].mean().reset_index()
    audience_type['Conversion Rate'] = audience_type['Conversion Rate'].map(format_percent)
    audience_type_pivot = audience_type.pivot(index='Type', columns='Target Audience', values='Conversion Rate').reset_index()
    st.dataframe(audience_type_pivot, use_container_width=True)

# --- Tab 5: Temporal Patterns ---
with tabs[4]:
    st.info("**Explore temporal and seasonal patterns in campaign performance.**")
    st.subheader("Temporal & Seasonal Patterns")

    # Revenue by Quarter
    st.markdown("#### Revenue by Quarter")
    filtered_df['Start Quarter'] = filtered_df['Start Date'].dt.quarter
    rev_quarter = filtered_df.groupby('Start Quarter')['Revenue'].mean().reset_index()
    fig_quarter = px.bar(
        rev_quarter, x="Start Quarter", y="Revenue", color="Start Quarter",
        title="Average Revenue by Quarter", labels={"Start Quarter": "Quarter", "Revenue": "Avg. Revenue"}
    )
    fig_quarter.update_yaxes(tickprefix="$", separatethousands=True, tickformat=".2f")
    st.plotly_chart(fig_quarter, use_container_width=True)

    # ROI by Month
    st.markdown("#### ROI by Month")
    filtered_df['Start Month'] = filtered_df['Start Date'].dt.month
    roi_month = filtered_df.groupby('Start Month')['ROI'].mean().reset_index()
    fig_month = px.line(
        roi_month, x="Start Month", y="ROI", markers=True,
        title="Average ROI by Month", labels={"Start Month": "Month", "ROI": "Avg. ROI"}
    )
    fig_month.update_yaxes(tickformat=".2f")
    st.plotly_chart(fig_month, use_container_width=True)

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