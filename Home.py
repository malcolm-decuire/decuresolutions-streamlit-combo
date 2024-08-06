
#s1- import dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from session_state import SessionState

#s1a set up the page 
st.set_page_config(page_title="Snowflake App", page_icon="🏡", layout="wide")
st.header("Snowflake App: Fintech & Adtech Fundamental Analysis ")
st.markdown("##")

#s1b progress bar
loading_page = "Please Wait 🤲🏽"
progress_text =loading_page
my_bar = st.progress(0, text=progress_text)
for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

#s1c - info to user remember to leave double spaces after each line '''
st.title("💡 Audience Takeaways")
st.write("📌 Learn about the Adtech & Real-Estate Industry")
st.write("📌 Learn how to deploy a Python app on Snowflake")
st.subheader("❓Target Audience")
st.write("🏘️ Real-Estate & 👨‍💻 Adtech Enthusiasts")

st.divider()

#s2 setup
st.header("📝 Visit 'Demo' page")
st.subheader("✏️ Select key filters like 'ticker', 'vertical', or 'score' ")
st.subheader("👉 Charts will update automatically")
st.caption("As of August-2024: Limited charting capabilities")
st.subheader("⏭️ Check 'Product Roadmap' page for upcoming features")

st.divider()

st.header("EODHD Fundamentals Data")
expander = st.expander("about vendor ")
expander.write('''
EOD Historical Data (EODHD) is a financial data provider that offers a variety of financial data through APIs. 
This data can be used to integrate into projects for stocks, ETFs, funds, indices, futures, bonds, options, forex pairs, and alternative currencies. \
    EODHD offers both free and paid plans
''')
expander.image("pages/photos/streamlit1.jpg")
st.subheader("⚠️ we created a custom sheet by combining statements (Balance/Cashflow/Income) from EODHD Fundamentals for demo purposes only" )

#s2 Utilize the local excel file & link to the source of the data 
def main():
    uploaded_file = st.file_uploader("", type=["xlsx"])

    if uploaded_file is not None:
        eodhd_df = pd.read_excel(uploaded_file, sheet_name=None)
    else:
        # for cloud & local deployment use a default file path (update as needed)
        file_path = "EODHD_ANNUAL_COMBINED_CLEANED_v2.xlsx"
        eodhd_df = pd.read_excel(file_path, sheet_name=None)

    if eodhd_df:
        sheet_names = list(eodhd_df.keys())
        selected_sheet = st.selectbox("SELECT A STATMENT", sheet_names)

        # for cloud & local deployment display the selected sheet's data
        st.dataframe(eodhd_df[selected_sheet])

if __name__ == "__main__":
    main()

#s3b create next section on pg
st.divider()

#s4
#placeholder for media 

#s5a progress bar reload 
st.button("🔄 Reload")