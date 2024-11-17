import streamlit as st

# --- PAGE SETUP ---
project_1_page = st.Page(
    page = "/Users/danishaziz/Desktop/danish/streamlit_multipage_app/views/worksheetEvaluator.py",
    title = "Worksheet Evaluator",
    icon = ":material/robot_2:",
    default=True,



)


project_2_page = st.Page(
    page = "/Users/danishaziz/Desktop/danish/streamlit_multipage_app/views/chatbot.py",
    title="Chat Bot",
    icon = ":material/smart_toy:",


)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
pg = st.navigation(pages=[project_1_page, project_2_page])

# --- SHARED ON ALL PAGES ---
st.logo("/Users/danishaziz/Desktop/danish/streamlit_multipage_app/assets/logo _infinity.jpg", size= "large")


# ---RUN NAVIGATION ---
pg.run()