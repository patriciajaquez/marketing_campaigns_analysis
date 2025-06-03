# 📈 Marketing Campaign Analysis

![Dashboard Banner](./img/banner_marketing_dashboard.png)

This project focuses on analyzing the performance of various marketing campaigns, including their return on investment (ROI), conversion rates, and revenue outcomes. It uses exploratory data analysis (EDA) techniques to extract meaningful insights that can inform future marketing strategies.

---

## 🎯 Project Objectives

- Analyze and visualize marketing campaign data.
- Identify top-performing and underperforming campaign types and channels.
- Compare ROI and conversion rates across different campaign segments.
- Categorize campaigns based on budget and effectiveness for better decision-making.

---

## 📊 Dataset Overview

The dataset contains **1,005 marketing campaigns** with the following attributes:

- **Campaign Details**: `Campaign Name`, `Start Date`, `End Date`, `Type`, `Channel`, `Target Audience`
- **Performance Metrics**: `Budget`, `ROI`, `Revenue`, `Net Profit`, `Conversion Rate`, `Cost Per Conversion`
- **Categorical Features**: `ROI Category`, `Conversion Category`, `High Budget Flag`, `High Roi Flag`
- **Date Features**: `Start Year`, `Start Month`, `Start Quarter`

---

## 🧹 Data Preparation

- Treated missing values and handled outliers.
- Extracted temporal features from campaign start dates.
- Created new features like ROI and conversion categories.
- Engineered flags for high-budget and high-ROI campaigns.

---

## 📊 Key Insights

- **Promotion** is the most frequently used marketing channel.
- **Organic** campaigns have the highest average ROI; **paid** campaigns have the highest median ROI.
- **Social media** campaigns generate the highest average revenue.
- **Webinar** campaigns achieve the highest average conversion rates.
- There is **no statistically significant difference** in conversion rates between B2B and B2C audiences.
- The top campaign by net profit is an organic podcast campaign with exceptionally high ROI.
- There is a positive relationship between budget and revenue, but increasing budget does not always guarantee higher revenue or ROI.
- **534 campaigns** have ROI > 0.5 and revenue > $500,000, most frequently associated with organic and promotion channels.
- ROI peaks in Q1 and Q4, while revenue peaks in Q2 and Q3, indicating seasonal effects.

## 🧮 How Insights Are Calculated

- ROI, revenue, and conversion rates are recalculated and formatted for clarity.
- Outliers and missing values are handled as described in the data preparation section.
- All summary tables and charts reflect the current filter selections in the dashboard.

---

## 📈 Tools & Libraries

- `Python`, `Pandas`, `NumPy`
- `Matplotlib`, `Seaborn`
- `Jupyter Notebook`
- `missingno`
- `scipy`
- `fuzzywuzzy`
- `streamlit`
- `plotly`

---

## 📁 Project Structure

<pre lang="text">
m1project_marketing_analysis/
│
├── data/
│   ├── raw/
│   │   └── marketingcampaigns.csv
│   └── processed/
│       └── marketingcampaigns_clean.csv
│
├── notebooks/
│   ├── eda.ipynb
│   └── preprocessing.ipynb
│
├── images/
│   └── banner_marketing_dashboard.png
│
├── eda_app.py
│ 
└── README.md
</pre>

---

## 🧠 Dashboard Banner

The image was generated using **DALL·E** with this prompt:

> A dashboard-style layout with dynamic marketing analytics displayed against a dark backdrop, featuring charts and graphs in vibrant shades of blue, orange, green, and teal. Includes pie chart, donut chart, bar graphs, and line graph. Clean and modern design. No text or labels.

To generate a similar image:
- Use [DALL·E](https://openai.com/dall-e) or Stable Diffusion.
- Specify "no text", "dashboard", "marketing analytics", and "data visualization" in the prompt.
- Choose a **wide format** (website banner style).

---

## ▶️ How to Run the Project

1. Clone the repo:
   ```bash
   git clone https://github.com/patriciajaquez/m1project_marketing_analysis.git
   cd m1project_marketing_analysis
   ```
2. Launch Jupyter Notebook:
   ```bash
   jupyter notebook notebooks/eda.ipynb
   ```
3. Explore the step-by-step analysis in the notebook.

---

## 📊 Interactive EDA App

You can explore the marketing campaign data interactively using the Streamlit dashboard:

### How to launch the app

1. Make sure you have all dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
   (Or manually install: streamlit, pandas, matplotlib, seaborn)
2. Run the Streamlit app:
   ```bash
   streamlit run eda_app.py
   ```
3. Use the sidebar filters to select channels and target audiences, and explore ROI distributions and other visualizations.

> **Note:** All dashboard insights and visualizations update dynamically based on your filter selections in the sidebar.

**Features:**
  - Filter campaigns by channel, type, audience, ROI, revenue, and date range
  - Visualize campaign distributions by channel and type
  - Compare performance metrics (ROI, revenue, conversion rate) by channel and type
  - Analyze conversion rates by audience, channel, and campaign type (including grouped comparisons)
  - Explore temporal patterns (by month and quarter)
  - View top campaigns by net profit, ROI, and conversion rate
  - All tables and charts update dynamically based on sidebar filters

---

👩‍💻 Author

Patricia Jáquez
Data Analyst & AI Bootcamp – Upgrade Hub

🔗[LinkedIn](https://www.linkedin.com/in/patricia-jaquez/)

---

📝 License

This project is part of a Bootcamp and intended for educational purposes. Feel free to use or adapt it with proper attribution.
