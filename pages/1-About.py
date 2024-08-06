#s1 import dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from session_state import SessionState

#s1 set up the page 
st.set_page_config(page_title="ABOUT", page_icon="❓", layout="wide")
st.title("Background")
st.markdown("##")


#s1a - progress bar
loading_page = "Please Wait 🤲🏽"
progress_text =loading_page
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

#s1 user info 
st.title("❓ About the Author")
expander = st.expander("Malcolm Decuire II")
expander.write('''
### 1. Strong Technical Expertise:
- I possess a solid foundation in engineering principles, with hands-on experience in both software and hardware technologies.
- My technical background allows me to understand complex systems and solutions, enabling me to effectively communicate technical details to clients and stakeholders.

### 2. Proven Sales Acumen:
- I have a track record of successfully identifying customer needs and aligning them with appropriate technical solutions.
- My ability to bridge the gap between technical teams and customers has consistently resulted in closing deals and driving revenue growth.

### 3. Excellent Communication Skills:
- I excel in translating technical jargon into clear, understandable language for non-technical audiences.
- My presentation and negotiation skills help me articulate the value of our solutions, fostering trust and building long-term client relationships.

### 4. Problem-Solving and Innovation:
- I am adept at diagnosing client challenges and developing tailored solutions that meet their specific requirements.
- My proactive approach to identifying opportunities for product and process improvement ensures that we deliver cutting-edge solutions that stay ahead of the competition.
''')


st.title("❓ Why should you care")
st.header("💰: Increase your investment acumen")
st.link_button("🔗 Value Investing","https://www.reddit.com/r/algotrading/comments/93pbwk/using_the_piotroski_f_score_as_a_factor/")

#s1b background about REIT
st.title("❓ What are REITs")
st.subheader("5-min. read on REITs")
st.link_button("🔗 LinkedIn Post", "https://www.linkedin.com/pulse/reits-everything-you-need-know-credence-family-office/")


#s1 addtil info- piot
st.title("❓ Why learn about Piotroski")
st.link_button("🔗 Quick LinkedIn Summary","https://www.linkedin.com/pulse/piotroski-f-score-its-importance-understanding-/")

#s1c addtl user guide- eod
st.title("❓ What is EODHD")
st.header("EODHD is a French based SaaS firm that offers Robust, powerful and easy to use APIs & Ready-to-go solutions")
st.link_button("🔗 Python docs", "https://eodhd.com/financial-apis/python-financial-libraries-and-code-samples/")


#s1a page setup-Style  Allow user to upload their own file
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#s1c page setup- guide 
st.title('❓ Why choose EODHD data')
st.divider()
st.write('1. Trade-off between free datasets that bored me vs paid-ones that didnt 😅')
st.write('2. Needed access to historical data without massive annual contracts (bloomberg is expensive)')
st.write('3. Its easier to work with data in environments Im already familiar with like Google Sheets, pandas, pyspark, etc')
st.write('4. :blue[Experiement with rapid-prototyping to simiulate commercial deadlines]')


#s1d addtl page set up 
st.divider()

#s2b reload 
st.button("🔄 Reload")