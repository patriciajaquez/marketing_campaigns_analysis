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

- **Campaign Details**: `campaign_name`, `start_date`, `end_date`, `type`, `channel`, `target_audience`
- **Performance Metrics**: `budget`, `roi`, `revenue`, `net_profit`, `conversion_rate`, `cost_per_conversion`
- **Categorical Features**: `roi_category`, `conversion_category`, `high_budget_flag`, `high_roi_flag`
- **Date Features**: `start_year`, `start_month`, `start_quarter`

---

## 🧹 Data Preparation

- Treated missing values and handled outliers.
- Extracted temporal features from campaign start dates.
- Created new features like ROI and conversion categories.
- Engineered flags for high-budget and high-ROI campaigns.

---

## 📊 Key Insights

- **Email** and **social media** campaigns show the highest ROI on average.
- **B2C** campaigns tend to have higher conversion rates compared to **B2B**.
- **Organic** and **promotion** channels outperform **paid** in ROI.
- Most campaigns with high budget do not guarantee high performance.

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

**Features:**
  - Filter campaigns by channel and target audience
  - Visualize ROI by channel (boxplot)
  - View filtered data in a table
  - Easily extend with more visualizations

---

👩‍💻 Author

Patricia Jáquez
Data Analyst & AI Bootcamp – Upgrade Hub

🔗[LinkedIn](https://www.linkedin.com/in/patricia-jaquez/)

---

📝 License

This project is part of a Bootcamp and intended for educational purposes. Feel free to use or adapt it with proper attribution.
