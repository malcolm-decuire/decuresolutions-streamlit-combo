#20240806 Updated EODHD example 

############################
#s1 import dependencies 
###########################
import streamlit as st
import time 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as pg
from session_state import SessionState
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
 
#s1a page setup  
st.set_page_config(page_title="Demo", page_icon="📈", layout="wide")
st.subheader("📊 Piotroski Analysis Demo")
st.markdown("##")

#s1b Style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#s1c local data load for beginners & users with minimal time
def load_data(file_path, sheet_name):
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name,  index_col=0, parse_dates=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

#s1a - progress bar
loading_page = "Please Wait 🤲🏽"
progress_text =loading_page
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()


#1c project info guide  
st.header("Overview:")
st.write("The Piotroski method evaluates a company's financial strength using nine accounting-based criteria")
st.write("### Examples of Analysis to Combine with the Piotroski Method:")
st.write("- **Value Investing**: To identify undervalued stocks with strong fundamentals.")
st.write("- **Growth Investing**: To assess the financial health of growing companies.")
st.write("- **Technical Analysis**: To time entries and exits based on price trends.")
st.write("- **Quality Investing**: To filter high-quality stocks with strong financials.")
st.write("- **Momentum Investing**: To find financially solid companies with upward price momentum.")
st.write("- **Factor Investing**: As one of multiple factors (e.g., value, size, quality) in a multifactor strategy.")

############################
#s2 XLSX upload
###########################
#s2a Read Excel sheets
combo_bs = pd.read_excel('EODHD_ANNUAL_COMBINED_CLEANED_v2.xlsx', sheet_name='balance_statements')
combo_cf = pd.read_excel('EODHD_ANNUAL_COMBINED_CLEANED_v2.xlsx', sheet_name='cashflow_statements')
combo_is = pd.read_excel('EODHD_ANNUAL_COMBINED_CLEANED_v2.xlsx', sheet_name='income_statements')

#s2b Merge DataFrames on 'filing_date' and 'ticker' columns
merged_combo_bs_is = pd.merge(combo_bs, combo_is, on=['filing_date', 'ticker'], how='outer')
merged_df = pd.merge(merged_combo_bs_is, combo_cf, on=['filing_date', 'ticker'], how='outer')

#s2c Function to calculate Piotroski F-Score
def calculate_piotroski_f_score(df):
    df['Profitability'] = df['netIncome_x'] > 0
    df['Operating Cash Flow'] = df['totalCashFromOperatingActivities'] > 0
    df['ROA'] = df['netIncome_x'] / df['totalAssets']
    df['Cash ROA'] = df['totalCashFromOperatingActivities'] / df['totalAssets']
    df['Delta ROA'] = df['ROA'].diff()
    df['Accruals'] = df['netIncome_x'] - df['totalCashFromOperatingActivities']
    df['Delta Leverage'] = -(df['longTermDebt'] - df['longTermDebt'].shift(1))
    df['Delta Current Ratio'] = df['otherCurrentAssets'] / df['totalCurrentLiabilities']
    df['Delta Shares Outstanding'] = -(df['commonStockSharesOutstanding'] - df['commonStockSharesOutstanding'].shift(1))

    df['Piotroski F-Score'] = (
        df['Profitability'].astype(int) +
        df['Operating Cash Flow'].astype(int) +
        (df['ROA'] > 0).astype(int) +
        (df['Cash ROA'] > 0).astype(int) +
        (df['Delta ROA'] > 0).astype(int) +
        (df['Accruals'] > 0).astype(int) +
        (df['Delta Leverage'] > 0).astype(int) +
        (df['Delta Current Ratio'] > 0).astype(int) +
        (df['Delta Shares Outstanding'] > 0).astype(int)
    )

    return df

#s2d Calculate F-Score and update session state
merged_df = calculate_piotroski_f_score(merged_df)
st.session_state.merged_df = merged_df

#s2e Data formatting 
# List of columns to appear first
cols_to_front = ['vertical', 'ticker', 'filing_date', 'Piotroski F-Score', 'ROA', 'Delta ROA']

# Rearrange the DataFrame columns
formatted_df = merged_df[cols_to_front + [col for col in merged_df.columns if col not in cols_to_front]]

# Update session state with the rearranged DataFrame
st.session_state.merged_df = formatted_df

############################
#s3 Interactive Table
###########################
st.divider()
st.header("Custom Data Methodology")
with st.popover("Filter Warnings"):
    st.markdown("⚠️ Columns to avoid")
    name = st.write("(exclude: earningAssets, accumulatedAmortization, negativeGoodwill)")
expander = st.expander("EODHD Data Integration Guide")

expander.write('''
To efficiently manage and analyze financial data using EOD Historical Data (EODHD) in Google Sheets, follow these steps:

### 1. Importing EODHD Data into Google Sheets:
- Utilize the EODHD API to pull financial data directly into Google Sheets using the `IMPORTDATA` or `IMPORTXML` functions.
- Create dedicated sheets for each financial statement (e.g., Income Statement, Balance Sheet, Cash Flow Statement).
- Automate data retrieval with Google Apps Script to ensure regular updates.

### 2. Adding Columns for Vertical and Ticker:
- **Vertical Column**: Add a "Vertical" column in each sheet to categorize the data by industry or sector.
- **Ticker Column**: Add a "Ticker" column in each sheet to identify the specific company associated with each financial entry.

### 3. Streamlining the Process for Multiple Financial Statements:
- Repeat the process for each financial statement: create a sheet, import data, and add "Vertical" and "Ticker" columns.
- Standardize formatting and structure across all sheets for consistency.

### 4. Ensuring Data Integrity and Consistency:
- Regularly review and validate imported data for accuracy.
- Use conditional formatting or data validation rules to ensure consistency in the "Vertical" and "Ticker" entries.

By following these steps, you can create a robust and organized system for analyzing EODHD data within Google Sheets, enabling better decision-making and financial analysis.
''')
expander.image("pages/photos/streamlit2.jpg")

#s3a Interactive Data Filter
def filter_dataframe(df):
    modify = st.checkbox("Activate Filters")
    if not modify:
        return df

    df = df.copy()

    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df


#s3b Display filtered DataFrame
filtered_df = filter_dataframe(st.session_state.merged_df)
st.dataframe(filtered_df)


# Display the schema of the DataFrame
# st.write("Schema of merged_df:")
# st.write(merged_df.dtypes) 

# Sort and Group the DataFrame
df2 = st.session_state.merged_df.sort_values(by="vertical")
df2['counter'] = df2.groupby('vertical').cumcount() + 1
df2['counter'] = pd.to_numeric(df2['counter'])

############################
#s4 Graph
###########################
st.divider()
st.header("Score Summary")
expander = st.expander("Methodology")
expander.write('''
**Interpretation**: A higher score (7-9) suggests a financially strong company, while a lower score (0-3) may signal potential financial distress.
               The Piotroski Score is a 9-point system used to assess a company's financial health, especially for value investing. 
               Each point represents a positive sign of financial strength across three categories:

### Profitability (4 points):
1. **Net Income**: 1 point if positive.
2. **Operating Cash Flow**: 1 point if positive.
3. **Return on Assets (ROA)**: 1 point if positive.
4. **Accruals**: 1 point if cash flow from operations exceeds net income, indicating high-quality earnings.

### Leverage, Liquidity, and Source of Funds (3 points):
1. **Decrease in Leverage (Debt to Equity)**: 1 point if leverage decreases, showing improved financial stability.
2. **Increase in Current Ratio**: 1 point if the current ratio improves, indicating better short-term liquidity.
3. **No New Shares Issued**: 1 point if no new equity is issued, suggesting the company is not diluting shareholders.

### Operating Efficiency (2 points):
1. **Gross Margin**: 1 point if gross margin improves, reflecting better cost management or pricing power.
2. **Asset Turnover**: 1 point if asset turnover improves, indicating more efficient use of assets.

''')

expander_insights = st.expander("Piotroski Score and Industry Insights")

expander_insights.write('''

### Characteristics of Poor-Performing Companies:
**REIT**:
- A poorly performing REIT often suffers from high leverage ratios and limited access to capital, which hampers its ability to finance new projects or maintain existing properties. 
- These REITs may also experience low occupancy rates, driven by poor property locations or ineffective management strategies. 
- Additionally, they might have exposure to distressed or non-core assets, leading to inconsistent cash flows and vulnerability during economic downturns.

**AdTech**:                        
- A poorly performing AdTech company typically faces declining revenues due to ineffective ad targeting and low conversion rates, which can result from outdated technology or inadequate data analytics capabilities. 
- High customer churn and reliance on a few key clients make the company vulnerable to market shifts. 
- Furthermore, such companies often struggle to adapt to evolving privacy regulations, which can lead to costly compliance issues and erode consumer trust, further impacting their competitive position in the market.

**Expanded Analysis**: Q1'2025                         
''')

expander_insights.image("pages/photos/streamlit3.jpg")

#s4a Scatter plot
tab1, tab2 = st.tabs(["STREAMLIT FLAVOR", "PLOTLY FLAVOR"]) 
df = filtered_df
fig_scatter = px.scatter(
    df,
    x="filing_date",
    y="Piotroski F-Score",
    color='ticker',
    size='Piotroski F-Score',
    hover_data=["vertical","ticker","Piotroski F-Score","ROA"],
)
with tab1: 
    st.plotly_chart(fig_scatter, theme="streamlit", use_container_width=True,)
with tab2:
    st.plotly_chart(fig_scatter, theme=None, use_container_width=True)

#s4b Create and display charts
fig = px.bar(df2, x='filing_date', y='Piotroski F-Score', orientation='v', title="REIT & Adtech Scores")
with tab1: 
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    st.plotly_chart(fig, theme=None, use_container_width=True)

#s4c Color gradient bar chart
fig_gradient = px.bar(df2, x=df2['filing_date'], y=df2['Piotroski F-Score'],
                      hover_data=['ROA', 'Cash ROA'], color='ROA',
                      labels={'Piotroski F-Score':'Return on Assets'}, height=400)
with tab1: 
    st.plotly_chart(fig_gradient, theme="streamlit", use_container_width=True)
with tab2:
    st.plotly_chart(fig_gradient, theme=None, use_container_width=True)



